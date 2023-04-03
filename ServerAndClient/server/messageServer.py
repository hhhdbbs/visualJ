import socket
import threading
import json

class MessageServer:
    """
    服务器类
    """

    def __init__(self,parent):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections = list()
        self.__identities = list()
        self.__parent=parent
        self.__baseDir=None

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = self.__connections[user_id]
        identity = self.__identities[user_id]
        print('[Server] 用户', user_id, ' ' , identity['ip'], '建立消息连接')

        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                print('got buffer:',buffer)
                obj = json.loads(buffer)
                cmd=obj['cmd']
                self.__parent.receiveMessage(obj)
                # if cmd == 'loadContainer' or cmd == 'execTask':
                #     self.__parent.receiveMessage(obj)
                # else:
                #     print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 连接失效:', connection.getsockname(), connection.fileno())
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__identities[user_id] = None

    # def __broadcast(self, user_id=0, message=''):
    #     """
    #     广播
    #     :param user_id: 用户id(0为系统)
    #     :param message: 广播内容
    #     """
    #     for i in range(1, len(self.__connections)):
    #         if user_id != i and self.__connections[i]:
    #             self.__connections[i].send(json.dumps({
    #                 'sender_id': user_id,
    #                 'sender_nickname': self.__nicknames[user_id],
    #                 'message': message
    #             }).encode())

    def getIdByIp(self,ip):
        for i in range(1, len(self.__identities)):
            if self.__identities[i]['ip']==ip:
                return i
        return -1


    def sendMessage(self, id,info):
        m=json.dumps(info)
       # self.__connections[id].send(str(len(m)).encode())
        self.__connections[id].send(m.encode())

    def __waitForLogin(self, connection):
        # 尝试接受数据
        # noinspection PyBroadException
       # try:
            buffer = connection.recv(1024).decode()
            # 解析成json数据
            obj = json.loads(buffer)
            print(obj)
            # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
            if obj['type'] == 'connect':
                self.__connections.append(connection)
                self.__identities.append({
                    'ip':obj['ip'],
                    'host':int(obj['host']),
                    'isConnct':True
                })
                connection.send(json.dumps({
                    'id': len(self.__connections) - 1,
                    'baseDir':self.__baseDir
                }).encode())

                # 开辟一个新的线程
                thread = threading.Thread(target=self.__user_thread, args=(len(self.__connections) - 1,))
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
      #  except Exception:
      #      print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())

    def start(self,ip,host,baseDir):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind((ip,host))
        # 启用监听
        self.__socket.listen(10)
        print('[Server] 服务器正在运行......')

        # 清空连接
        self.__connections.clear()
        self.__identities.clear()
        self.__connections.append(None)
        self.__identities.append('System')
        self.__baseDir=baseDir

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(), connection.fileno())

            thread = threading.Thread(target=self.__waitForLogin, args=(connection,))
            thread.setDaemon(True)
            thread.start()

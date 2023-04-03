from re import T
import socket
import threading
import json
import os
from client.fileClient import FileClient
import requests

class MessageClient():
    """
    客户端
    """
    def __init__(self,parent):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__fileClient=FileClient(self)
        self.__id = None
        self.__isConnect = False
        self.__ipH=None
        self.__parent=parent
        self.__baseDir=None
        self.__identity=None

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while self.__isConnect:
            # noinspection PyBroadException
           # try:
                buffer = self.__socket.recv(1024).decode()
                print(buffer)
                obj = json.loads(buffer)
                cmd=obj['cmd']
                if cmd=='loadContainer':
                    id=obj['id']
                    parameters=obj['parameters']
                    containername=obj['containername']
                    s='sh loadContainer.sh {0}'.format(parameters)
                    print('执行命令 ',s)
                    os.system(s)
                    print ('loaded container', containername)
                    self.do_send({'sender_id': self.__id,'cmd':'loadContainer','id':id,'result':'success','containername':containername,'status':4})
                elif cmd=='execTask':
                    parameters=obj['parameters']
                    workFilename=obj['workFilename']
                    outputs=obj['outputs']
                    containername=obj['containername']
                    id=obj['id']

                    s='sh runContainer.sh {0} {1} ,{2}'.format(containername,workFilename,parameters)
                    print('执行命令 ',s)
                    n=os.system(s)
                    print ('执行完毕')
                    # for out in outputs:
                    #     f = open(out,'wb')
                    #     f.close()

                    #
                    self.do_send({'sender_id': self.__id,'cmd':'execTask','id':id,'result':'success','status':4})
                    
                    for out in outputs:
                        data = {"name" : os.path.basename(out)}
                        files = {
                            "file" : open(out, "rb")
                            }
                        r = requests.post("http://192.168.1.202:8082/app/get_work_output_img/", data, files=files)

                    self.do_send({'sender_id': self.__id,'cmd':'execTask','id':id,'taskID':taskID,'nodeID':nodeID,'result':'success','status':5})



                    

           # except Exception:
               # print('[Client] 无法从服务器获取数据')

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self.__socket.send(json.dumps(message).encode())

    def start(self,serverip,serverh,__ip,__h,__identity):
        """
        启动客户端
        """
        self.__socket.connect((serverip,serverh))
        self.__ipH=(__ip,__h)
        self.__identity=__identity
        self.do_connect()
        while True:
            a=1

    def do_connect(self):
        # 将昵称发送给服务器，获取用户id
            self.__socket.send(json.dumps({
            'type': 'connect',
            'ip': self.__identity,
            'host':self.__ipH[1]
        }).encode())
        # 尝试接受数据
        # noinspection PyBroadException
        # try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self.__id = obj['id']
                self.__baseDir=obj['baseDir']
                self.__isConnect = True
                print('[Client] 连接到服务器 ')
                # 开启子线程用于接受数据
                thread = threading.Thread(target=self.__receive_message_thread)
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] 连接到服务器失败')
        # except Exception:
        #     print('[Client] 无法从服务器获取数据')


    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        # 显示自己发送的消息
        print('[' + str(self.__ipH) + '(' + str(self.__id) + ')' + '] send :', message)
        # 开启子线程用于发送数据
        thread = threading.Thread(target=self.__send_message_thread, args=(message,))
        thread.setDaemon(True)
        thread.start()


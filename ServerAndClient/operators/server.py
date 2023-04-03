import socketserver,os
from time import sleep
import threading

from django import db
#from server.fileServer import FileServer
from server.messageServer import MessageServer
import pymysql
from server.mysqlServer import MysqlServer
import json
from server.fileClient import FileClient

class Server():
    def __init__(self):
        """
        构造
        """
        self.__messageServer = MessageServer(self)
        self.__fileClient=FileClient(self)
        self.__sqlLock = threading.Lock()
        self.__mysqlServer = MysqlServer(self,self.__sqlLock)
        self.__dir=None

    def start(self):
        with open('./settings.json','r',encoding='utf8')as f:
            load_dict=json.load(f)
        self.__dir=load_dict['dir']

        thread = threading.Thread(target=self.__messageServer.start,args=('127.0.0.1', 80))
        thread.setDaemon(True)
        thread.start()

        thread = threading.Thread(target=self.__mysqlServer.start)
        thread.setDaemon(True)
        thread.start()

      #  self.__messageServer.start()
        #server.sendMessage('192.32.12.2',{'cmd':'loadContainer','operatorDistributeID':2,'parameters':'pa','containername':'strghenC'})
        while True:
            a=1
          #  server.sendMessage('192.32.12.2',{'cmd':'loadContainer','operatorDistributeID':2,'parameters':'pa','containername':'strghenC'})
            
           # server.sendMessage('192.32.12.2',{'cmd':'execTask','parameters':'pa','taskID':2,'nodeID':3})
        #instance = socketserver.ThreadingTCPServer(('127.0.0.1',9999),FileServer)            
        #instance.serve_forever()
       # self.sendMessage('192.32.12.2',)        

    def getDirsByIp(self,ip):
        return self.__mysqlServer.getDirsByIp(ip)

    def receiveMessage(self,obj):
        print(obj)
        cmd=obj['cmd']
        if cmd == 'loadContainer':
            id=int(obj['id'])
            result=obj['result']#succcess
            containername=obj['containername']
            self.__sqlLock.acquire()
            print(id,' containername:' ,containername,'装载完成')
            self.__mysqlServer.setOperatorDistributeStatus(id,4)
            self.__sqlLock.release()
        elif cmd == 'execTask':
            taskID=obj['taskID']
            nodeID=obj['nodeID']
            result=obj['result']

    def sendMessage(self,ip,message):
        print(message)
        id=self.__messageServer.getIdByIp(ip)
        if id==-1:
            print('目标主机',ip,'未建立连接')
        else:
            self.__messageServer.sendMessage(id,message)

    def sendImgs(self,id,ip,port,inputs,imgDir):
        thread = threading.Thread(target=self.__fileClient.sendImgs,args=(id,ip,port,self.__dir,inputs,imgDir))
        thread.setDaemon(True)
        thread.start()
        
    def sendContainerFile(self,id,ip,port,filelocation,filename,operatorDir):
            thread = threading.Thread(target=self.__fileClient.sendContainerFile,args=(id,ip,port,os.path.join(self.__dir,filelocation),filename,operatorDir))
            thread.setDaemon(True)
            thread.start()

    def receiveFileMessage(self,obj):
        cmd=obj['cmd']
        if cmd=='container':
            self.__sqlLock.acquire()
            self.__mysqlServer.setOperatorDistributeStatus(obj['id'],obj['status'])
            self.__sqlLock.release()
            if obj['message']=='fail':
                print('container ',obj['id'],'传输失败')
            else:
                print('container ',obj['id'],'传输成功')
        elif cmd=='inputImg':
            self.__sqlLock.acquire()
            self.__mysqlServer.setNodeStatus(obj['id'],obj['status'])
            self.__sqlLock.release()
            if obj['message']=='fail':
                print('imgs ',obj['id'],'传输失败')
            else:
                print('imgs ',obj['id'],'传输成功')
server=Server()
server.start()
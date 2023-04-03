from ast import arg
from re import T
from time import sleep
from client.messageClient import MessageClient
from client.fileServer import FileServer
import socketserver
import threading
class Client():
    def __init__(self):
        self.__messageClient=MessageClient(self)
        self.__dirInit=False
        self.__ipH=('127.0.0.1',8084)#文件接收端口
        self.__serveripH=('192.168.1.202',8083)#消息发送端口
        self.__identity='192.168.1.203'#文件接收端口


    def start(self):
        # thread = threading.Thread(target=self.__messageClient.start,args=(self.__serveripH[0],self.__serveripH[1],self.__ipH[0],self.__ipH[1],self.__identity))
        # thread.setDaemon(True)
        # thread.start()

        instance = socketserver.ThreadingTCPServer(self.__ipH,FileServer)            
        instance.serve_forever()
    

client = Client()
client.start()

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
        self.__ipH=('127.0.0.1',9999)#文件接收端口
        self.__serveripH=('127.0.0.1',80)#消息发送端口
        self.__TCPthreadipH=('127.0.0.1',12)#文件发送端口


    def start(self):
        thread = threading.Thread(target=self.__messageClient.start,args=(self.__serveripH[0],self.__serveripH[1],self.__TCPthreadipH[0],self.__TCPthreadipH[1]))
        thread.setDaemon(True)
        thread.start()

        instance = socketserver.ThreadingTCPServer(self.__ipH,FileServer)            
        instance.serve_forever()
    

client = Client()
client.start()

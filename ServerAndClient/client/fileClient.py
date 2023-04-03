from ast import operator
import socket,os

class FileClient():
    def __init__(self,parent):
        self.__parent=parent

    def sendImgs(self,ip,port,baseDir,outputs):
            ip_port = (ip,port)
            sk = socket.socket()
            sk.connect(ip_port)
 
            for out in outputs:
                filepath=out
                filename=os.path.basename(filepath)
                target=os.path.join(baseDir,filename)
                print(target)
                file_size = os.stat(filepath).st_size
                sk.send(("imgs|"+target+"|"+str(file_size)).encode())

                send_size = 0
                f = open(filepath,'rb')
                Flag = True
                while Flag:
                    if send_size + 1024 > file_size:
                       data = f.read(file_size - send_size)
                       Flag = False
                    else:
                        data = f.read(1024)
                        send_size += 1024
                    sk.send(data)
                f.close()
            sk.close()


    def sendContainerFile(self,id,ip,port,filelocation,filename,operatorDir):
     #   try:
            ip_port = (ip,port)
            sk = socket.socket()
            sk.connect(ip_port)
            print(operatorDir)
            print(filename)
            target=os.path.join(operatorDir,filename)
            file_size = os.stat(filelocation).st_size
            print("container|"+target+"|"+str(file_size))
            sk.send(("container|"+target+"|"+str(file_size)).encode())
            send_size = 0
            f = open(filelocation,'rb')
            Flag = True
            while Flag:
                if send_size + 1024 > file_size:
                   data = f.read(file_size - send_size)
                   Flag = False
                else:
                    data = f.read(1024)
                    send_size += 1024
                sk.send(data)
            f.close()
            sk.close()
            self.__parent.receiveFileMessage({'id':id,'cmd':'container','message':'success','status':2})
        # except:
        #     self.__parent.receiveFileMessage({'id':id,'cmd':'container','message':'fail','status':0})
    
#!/usr/bin/env python
#_*_ encoding=utf-8 _*_
 
 
import socket,sys,os



filelocation=sys.argv[1]
filename=sys.argv[2]
operatorDir=sys.argv[3]

ip_port = ("127.0.0.1",8084)
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
    print("container|"+target+"|"+str(send_size)+"|"+str(file_size))
f.close()
sk.close()
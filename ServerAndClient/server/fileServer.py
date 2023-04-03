#!/usr/bin/env python
# _*_ encoding=utf-8 _*_
 
import socketserver,os
import json
class FileServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        print('connected...')
        while True:

            pre_data = conn.recv(1024).decode()
            print('got cmd:',pre_data)
            #获取请求方法，文件名，文件大小
            cmd,filepath,file_size = pre_data.split('|')
            #已经接收文件的大小
            recv_size = 0
            #上传文件路径拼接
            f = open(filepath,'wb')
            Flag = True
            while Flag:
                #未上传完毕
                if int(file_size)>recv_size:
                    data = conn.recv(1024)
                    recv_size += len(data)
                else:
                    recv_size = 0
                    Flag = False
                    continue
                #写入文件
                f.write(data)
            print('upload successed')
            f.close()
            
    
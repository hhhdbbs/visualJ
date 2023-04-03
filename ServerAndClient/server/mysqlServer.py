from ast import operator
from time import sleep
import pymysql
import threading
import json
import datetime
class MysqlServer:
    """
    服务器类
    """

    def __init__(self,parent,__sqlLock):
        self.__parent=parent
        self.__db=None
        self.__lock = __sqlLock

    def start(self):
        thread = threading.Thread(target=self.chectDistributeWait)
        thread.setDaemon(True)
        thread.start()

        thread = threading.Thread(target=self.chectNodeWait)
        thread.setDaemon(True)
        thread.start()

    def getCursor(self):
        self.__db = pymysql.connect(database='visual',host="127.0.0.1", user="root", password="123456", port=3306)
        cursor = self.__db.cursor()
        return cursor

    def chectNodeWait(self):
        while True:
            self.__lock.acquire()
            cursor=self.getCursor()

            sql = "SELECT * FROM task_node_wait where status =0"
            cursor.execute(sql)
            task_node_wait = cursor.fetchone()
            upt=[]
            while task_node_wait != None:
                if task_node_wait[13].replace(" ", "")=="":
                    upt.append(task_node_wait)
                task_node_wait = cursor.fetchone()
            for item in upt:
                sql = "UPDATE task_node_wait SET status ={0}  WHERE id={1}".format(1,item[0])
                cursor.execute(sql)
                sql = "UPDATE task_node_status SET status ='{0}'  WHERE node_id={1} and task_id={2}".format("Waiting",item[16],item[17])
                # print(sql)
                cursor.execute(sql)
                print(item[0]," status to 1", )
            cursor.close()
            self.__db.commit()

            cursor=self.getCursor()
            #
            sql = "SELECT * FROM task_node_wait where status =1 or status=2"
            cursor.execute(sql)
            upt1=[]
            upt2=[]
            row = cursor.fetchone()
            while row != None:
                id=row[0]
                status=row[2]
                start_time=row[18]
                if status==1:
                    upt1.append(row)
                elif status==2:
                    now_time=datetime.datetime.now()
                    if now_time>datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'):
                        upt2.append(row)
                row = cursor.fetchone()

            print("upt1 ",upt1)
            for item in upt1:
                print(item," status to 2", )
                self.setNodeStatus(item[0],2,item)
            print("upt2 ",upt2)
            for item in upt2:
                print(item," end", )
                self.setNodeStatus(item[0],3,item)
            cursor.close()
            self.__lock.release()
            sleep(4)




    def chectDistributeWait(self):
        while True:
            sleep(10)

    def setOperatorDistributeStatus(self,id,status):
        sql = "UPDATE distribute_wait SET status ={0}  WHERE id={1}".format(status,id)
        cursor=self.getCursor()
        cursor.execute(sql)
        # if status==4:
        #     sql = "DELETE FROM distribute_wait WHERE id={0}".format(id)
        #     cursor.execute(sql)
        cursor.close()
        self.__db.commit()

    def setNodeStatus(self,id,status,row):
        cursor=self.getCursor()
        if status==2:
            sql = "SELECT * FROM container where busy=0 and status = '正常'"
            cursor.execute(sql)
            container = cursor.fetchone()
            if container!=None:
                node_id=row[16]
                task_id=row[17]
                sql = "UPDATE task SET status ='Run'  WHERE id={0}".format(task_id)
                cursor.execute(sql)
                sql = "UPDATE task_node_wait SET status = {0} WHERE id={1}".format(status,id)
                cursor.execute(sql)
                sql = "UPDATE container SET busy =1  WHERE id={0}".format(container[0])
                # print(sql)
                cursor.execute(sql)
                sql = "UPDATE task_node_status SET server = {0} WHERE task_id={1} and node_id={2}".format(container[0],task_id,node_id)
                # print(sql)
                cursor.execute(sql)
                sql = "UPDATE task_node_status SET status='Run' WHERE task_id={1} and node_id={2}".format(container[0],task_id,node_id)
                # print(sql)
                cursor.execute(sql)
                sql = "UPDATE task_node_wait SET start_time = '{0}'  WHERE id={1}".format((datetime.datetime.now()+datetime.timedelta(seconds=5)).strftime('%Y-%m-%d %H:%M:%S'),id)
                # print(sql)
                cursor.execute(sql)
                print(row[0]," 2 处理结束")
            else:
                print(row[0]," 2 无处理及 不处理")
        elif status==3:
            sql = "UPDATE task_node_wait SET status ={0}  WHERE id={1}".format(status,id)
            cursor.execute(sql)
            node_id=row[16]
            task_id=row[17]
            sql = "SELECT * FROM task_node_status WHERE task_id={0} and node_id={1}".format(task_id,node_id)
            # print(sql)
            cursor.execute(sql)
            task_node_status = cursor.fetchone()
            # print(task_node_status)
            sql = "UPDATE task_node_status SET status='End' WHERE id={0}".format(task_node_status[0])
            # print(sql)
            cursor.execute(sql)
            sql = "UPDATE container SET busy =0  WHERE id={0}".format(task_node_status[5])
            # print(sql)
            cursor.execute(sql)
            sql = "SELECT * FROM task_node_wait WHERE task_id={0} and status=0".format(task_id)
            # print(sql)
            cursor.execute(sql)
            task_node_wait = cursor.fetchone()
            upd=[]
            flag=True
            while task_node_wait!=None:
                preWaitIds=task_node_wait[13]
                if preWaitIds.replace(" ", "")!="":
                    flag=False
                pre_ids=preWaitIds.split(" ")
                n=len(pre_ids)
                bek=""
                for i in range(n):
                    if str(id) != pre_ids[i] and str(id) != ' ':
                        bek=bek+" "+pre_ids[i]
                upd.append({"bek":bek,"id":task_node_wait[0]})
                task_node_wait = cursor.fetchone()
            for item in upd:
                sql = "UPDATE task_node_wait SET preWaitIds ='{0}'  WHERE id={1}".format(item['bek'],item['id'])
                cursor.execute(sql)
            if flag:
                sql = "UPDATE task SET status ='End'  WHERE id={0}".format(task_id)
                cursor.execute(sql)
            print(row[0]," 3 处理结束")
        cursor.close()
        self.__db.commit()

    def getDirsByIp(self,ip):
        self.__lock.acquire()
        sql = "SELECT * FROM container"
        cursor=self.getCursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        while row:
            row_ip=row[2]
            if row_ip==ip:
                cursor.close()
                self.__lock.release()
                return {
                    'operatorDir':row[9],
                    'imgDir':row[10]
                }
            row = cursor.fetchone()
        cursor.close()
        self.__lock.release()
        return None




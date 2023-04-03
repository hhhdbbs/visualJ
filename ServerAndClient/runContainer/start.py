import os
import sys
def main(containername,managePy,parameters):
    s='sh ./run.sh {0} {1} {2}'.format(containername,managePy,parameters)
    print('执行命令 ',s)
    n=os.system(s)
    print ('执行完毕')
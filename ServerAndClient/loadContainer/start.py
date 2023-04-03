import os
import sys
#filelocation,imagename,containername,localDir,containerDir
def main(parameters):
    s='sh ./run.sh {0}'.format(parameters)
    print("执行命令 ",s)
    n=os.system(s)
    print ('load完毕')
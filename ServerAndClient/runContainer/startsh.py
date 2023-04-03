import os
import sys
containername=sys.argv[1]
dir=sys.argv[2]
input=sys.argv[3]
output=sys.argv[4]
s='sh ./run.sh {0} {1} {2} {3}'.format(containername,dir,input,output)
n=os.system(s)
print ('执行完毕')
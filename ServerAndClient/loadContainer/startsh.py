import os
import sys
#dir tar包 imgename
imageDir=sys.argv[1]
file=sys.argv[2]
file=os.path.join(imageDir,file)
imagename=sys.argv[3]
containername=sys.argv[4]
localDir=sys.argv[5]
containerDir=sys.argv[6]
s='sh ./run.sh {0} {1} {2} {3} {4}'.format(file,imagename,containername,localDir,containerDir)
n=os.system(s)
print ('load完毕')
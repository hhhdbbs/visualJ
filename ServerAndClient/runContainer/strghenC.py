import sys
import os
import shutil
dir=sys.argv[1]
input=sys.argv[2]
output=sys.argv[3]
srcFile=os.path.join(dir,input)
dstFile=os.path.join(dir,output)
shutil.copyfile(srcFile,dstFile)
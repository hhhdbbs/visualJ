import sys
from shutil import copyfile
inp=sys.argv[1]
output=sys.argv[2]
copyfile(inp, output)
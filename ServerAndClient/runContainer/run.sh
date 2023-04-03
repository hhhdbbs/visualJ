#!/bin.bash
echo "hello ${1} ${2} ${3}"
# $1 容器id
# 其他的是参数
sudo docker restart ${1} 
sudo docker exec -it ${1} /bin/bash -c "python3 ${2} ${3} && exit"
# python3 strghenC.py ${2} ${3}
# exit 0
sudo docker stop ${1}
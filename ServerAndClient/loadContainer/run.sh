#!/bin.bash
sudo docker load -i ${1}
sudo docker run -id --name=${3} -v ${4}:${5} ${2} /bin/bash
sudo docker stop ${3}
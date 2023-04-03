#!/bin.bash

# 
sudo docker restart ${1}
nump=$*
parameters=${nump#*,}

echo "ivic.cn" | sudo -S docker exec -it ${1} /bin/sh -c "${2} ${parameters} && exit"
# python3 strghenC.py ${2} ${3}
# exit 0
sudo docker stop ${1}

sudo docker run -id  \
    --name=${container_name} \
    -v ${local_input}:${container_input_dir} \
    -v ${local_output}:${container_output_dir} \
    ${image_name} /bin/sh
echo ${password} | sudo -S \
    docker exec -it ${1} /bin/sh \
    -c "${code} ${parameters} && exit"
sudo docker stop ${1}

sudo docker load -i ${file_location}
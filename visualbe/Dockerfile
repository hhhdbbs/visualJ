# 建立 python3.7 环境
 FROM python:3.6
 
 # 设置 python 环境变量
 ENV PYTHONUNBUFFERED 1
 
 # 设置pip源为国内源
 COPY pip.conf /root/.pip/pip.conf
 
 # 在容器内/var/www/html/下创建 mysite1文件夹
 RUN mkdir -p /src/visualbe
 
 # 设置容器内工作目录
 WORKDIR /src/visualbe
 
 # 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
 ADD . /src/visualbe
 
 # 利用 pip 安装依赖
 RUN pip install -r requirements.txt

  # Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除。
 RUN sed -i 's/\r//' ./start.sh
 
 # 设置start.sh文件可执行权限
 RUN chmod +x ./start.sh
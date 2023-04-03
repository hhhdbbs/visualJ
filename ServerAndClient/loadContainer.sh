#!/bin.bash
sudo docker load -i ${1}
sudo docker run -id --name=${3} -v ${4}:${5} ${2} /bin/sh
sudo docker stop ${3}

import luigi
class MyTask(luigi.Task):
    #填写任务执行参数
    param = ligi.Parameter(default=42)

    #描述目标任务所依赖的前置任务
    def requires(self):
        return SomeOtherTask(self.param)

    #描述任务的业务逻辑
    def run(self):
        f=self.output().open('w')
        print >>f,"hello world"
        f.close()

    #定义输出文件目录
    def output(self):
        return luigi.LocalTarget('/tmp/foo/bar-%s.txt' % self.param)

if __name__=='__main__':
    luigi.run()

apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-  # 工作流名称
spec:
  entrypoint: whalesay        # 将“whalesay”定义为“主要”模板
  templates:
  - name: whalesay            # 定义“whalesay”模板
    container:
      image: docker/whalesay
      command: [cowsay]
      args: ["hello world"]   # 该模板在“whalesay”图像中运行“cowsay”指令，参数为“hello world”。

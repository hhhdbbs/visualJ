from ast import operator
from statistics import mode
from symbol import parameters
from django.db import models
from django.db.models import CASCADE

class User(models.Model):
    account=models.CharField(max_length=64, blank=False)
    password=models.CharField(max_length=64, blank=False)
    isadmin=models.BooleanField()
    description=models.CharField(max_length=64, blank=False)
    class Meta:
        db_table = "user"
# 算子
class Operator(models.Model):
    name=models.CharField(max_length=64, blank=False)
    description=models.CharField(max_length=256)
    file=models.FileField(upload_to='operator', null=True, blank=True)
    filename=models.CharField(max_length=64, blank=False,unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    imagename=models.CharField(max_length=64, blank=False,unique=True)
    inputDir=models.CharField(max_length=64, blank=False)
    outputDir=models.CharField(max_length=64, blank=False)
    workFilename=models.CharField(max_length=64, blank=False)
    loading=models.BooleanField()

    class Meta:
        db_table = "operator"

class Operator_parameter(models.Model):
    operator = models.ForeignKey(Operator, on_delete=CASCADE)
    sequence = models.IntegerField(default=1)
    name=models.CharField(max_length=64, blank=False)
    parameter_type=models.CharField(max_length=64)
    description=models.CharField(max_length=64,default='')

    class Meta:
        db_table = "operator_parameter"

class Container(models.Model):
    name=models.CharField(max_length=64, blank=False, unique=True)
    ip=models.CharField(max_length=64, blank=False)
    port = models.IntegerField()
    description=models.CharField(max_length=256)
    CPU = models.IntegerField(default=1)
    capacity=models.CharField(max_length=32)
    username=models.CharField(max_length=64, blank=False)
    password=models.CharField(max_length=64, blank=False)
    operatorDir=models.CharField(max_length=64, blank=False)
    imgDir=models.CharField(max_length=64, blank=False)
    status=models.CharField(max_length=64, blank=False)
    busy=models.BooleanField()
    class Meta:
        db_table = "container"

class Operator_distribute(models.Model):
    operator = models.ForeignKey(Operator,on_delete=CASCADE)
    container = models.ForeignKey(Container,on_delete=CASCADE)
    containername=models.CharField(max_length=64, blank=False,unique=True)

    class Meta:
        db_table = "operator_distribute"

class Distribute_wait(models.Model):
    operator_distribute=models.ForeignKey(Operator_distribute,on_delete=CASCADE)
    parameters=models.CharField(max_length=512, blank=False)
    status=models.IntegerField()#0:未开始 1 文件正在传送 2 文件传送完成 3 文件正在load 4 文件load完成
    containername=models.CharField(max_length=256, blank=False)
    ip=models.CharField(max_length=64, blank=False)
    port = models.IntegerField()
    filename=models.CharField(max_length=64, blank=False)
    filelocation=models.CharField(max_length=256, blank=False)
    operatorDir=models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "distribute_wait"

class App(models.Model):
    name=models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "app"

class DAG_node(models.Model):
    operator=models.ForeignKey(Operator, on_delete=CASCADE)
    task_ID=models.IntegerField()
    App=models.ForeignKey(App, on_delete=CASCADE)
    pos_x=models.DecimalField(max_digits=6, decimal_places=2)
    pos_y=models.DecimalField(max_digits=6, decimal_places=2)
    node_type=models.CharField(max_length=64, blank=False, default='task')
    node_location=models.CharField(max_length=64, blank=False)
    class Meta:
        db_table = "DAG_node"

class DAG_node_circle(models.Model):
    node_circle=models.IntegerField()
    node=models.ForeignKey(DAG_node, on_delete=CASCADE)
    pos_x=models.DecimalField(max_digits=6, decimal_places=2)
    pos_y=models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = "DAG_node_circle"

class Node_parameter(models.Model):
    node=models.ForeignKey(DAG_node, on_delete=CASCADE)
    operator_parameter=models.ForeignKey(Operator_parameter, on_delete=CASCADE)
    value=models.CharField(max_length=64)
    export=models.BooleanField(default=False)

    class Meta:
        db_table = "node_parameter"

class DAG_line(models.Model):
    from_node_circle=models.ForeignKey(DAG_node_circle, on_delete=CASCADE,related_name='from_node_circle_id')
    to_node_circle=models.ForeignKey(DAG_node_circle, on_delete=CASCADE,related_name='to_node_circle_id')
    App=models.ForeignKey(App, on_delete=CASCADE)

    class Meta:
        db_table = "DAG_line"  

class Task(models.Model):
    app=models.ForeignKey(App, on_delete=CASCADE)
    name=models.CharField(max_length=64, blank=False, unique=True)
    input = models.ImageField(upload_to='task_img/input', null=True, blank=True)
    status=models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "task"  

class Task_node_status(models.Model):
    task=models.ForeignKey(Task, on_delete=CASCADE)
    node=models.ForeignKey(DAG_node,on_delete=CASCADE)
    status=models.CharField(max_length=32, blank=False)
    container=models.ForeignKey(Container, on_delete=CASCADE)
    server=models.IntegerField(null=True)#0 未load  1 等待照片传送 2 等待load
    class Meta:
        db_table = "task_node_status"  

class Task_node_wait(models.Model):
    start_time = models.CharField(max_length=512,null=True)
    parameters=models.CharField(max_length=512, blank=False)
    status=models.IntegerField()#0 未load  1 等待照片传送 2 等待load
    localInputDir=models.CharField(max_length=64, blank=False)
    localOutputDir=models.CharField(max_length=64, blank=False)
    imageInputDir=models.CharField(max_length=64, blank=False)
    imageOutputDir=models.CharField(max_length=64, blank=False)
    inputs=models.CharField(max_length=512, blank=False)
    outputs=models.CharField(max_length=512, blank=False)
    ip=models.CharField(max_length=64, blank=False)
    port = models.IntegerField()
    workFilename=models.CharField(max_length=64, blank=False)
    containername=models.CharField(max_length=256, blank=False)
    preWaitIds=models.CharField(max_length=64, blank=False)
    node_location=models.CharField(max_length=64, blank=False)
    task=models.ForeignKey(Task, on_delete=CASCADE)
    node=models.ForeignKey(DAG_node,on_delete=CASCADE)
    renameInputs=models.CharField(max_length=512, blank=False)
    class Meta:
        db_table = "task_node_wait" 


class Task_output(models.Model):
    task=models.ForeignKey(Task, on_delete=CASCADE)
    file_location=models.CharField(max_length=64, blank=False)
    name=models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = "task_output" 
    
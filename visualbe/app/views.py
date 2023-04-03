import datetime
import json
import random
import os
import re
import shutil
from django.conf import settings
from django.http import HttpResponse, JsonResponse, response
from app.models import *
from queue import Queue
import time
    
# 时间格式化
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)
    

def login(request):
    account=request.POST['account']
    password=request.POST['password']
    users=User.objects.filter(account=account).filter(password=password)
    data={}
    if len(users)==0:
        data={'result':False}
    else:
        data={'result':True,'isadmin':users[0].isadmin}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')
    
def user_list(request):
    ret=[]
    user_list=User.objects.all()
    for user in user_list:
        ret.append({
            'id':user.id,
            'account':user.account,
            'password':user.password,
            'description':user.description,
            'isadmin':user.isadmin
        })
    return HttpResponse(json.dumps(ret, cls=DateEncoder), content_type='application/json')

def create_user(request):
    account=request.POST['account']
    password=request.POST['password']
    isadmin=int(request.POST['isadmin'])
    description=request.POST['description']
    user=User()
    user.account=account
    user.password=password
    user.isadmin=isadmin
    user.description=description
    user.save()
    data = {
            'msg': '创建成功',
            'result':0,
            'id':user.id
        }
    return JsonResponse(data=data)

def delete_user(request):
    try:
        id = int(request.POST['id'])
        user = User.objects.get(pk=id)
        if user != None:
            user.delete()
            data = {'msg': '删除成功', 'status': 0}
        else:
            data = {'msg': '删除失败', 'status': 1}
    except:
        data = {'msg': 'wrong', 'status': 1}
    return JsonResponse(data=data)

def get_work_input_dir_basemedia():
    return os.path.join('work_img','input')

def get_work_dir():
    path=os.path.join(settings.BASE_DIR,'media')
    path=os.path.join(path,'work_img')
    return path

def get_task_input_dir():
    path=os.path.join(settings.BASE_DIR,'media')
    path=os.path.join(path,'task_img')
    path=os.path.join(path,'input')
    return path

def get_work_input_dir():
    path=os.path.join(get_work_dir(),'input')
    return path

def get_work_out_dir():
    path=os.path.join(get_work_dir(),'output')
    return path
    
def get_work_output_dir():
    path=os.path.join(get_work_dir(),'output')
    return path

def get_task_output_dir():
    path=os.path.join(settings.BASE_DIR,'media')
    path=os.path.join(path,'task_img')
    path=os.path.join(path,'output')
    return path

def get_export_dir():
    path=os.path.join(settings.BASE_DIR,'media')
    path=os.path.join(path,'task_img')
    path=os.path.join(path,'output')
    return path

def save_file(dir,chunks):
    destination = open(dir,'wb+')
    for chunk in chunks:
        destination.write(chunk)
    destination.close()

def get_DAG_info(appID):
    nodes=[]
    node_objects=DAG_node.objects.filter(App_id=appID)
    for node_object in node_objects:
        operator_object=Operator.objects.get(pk=node_object.operator_id)
        operator_parameters=Operator_parameter.objects.filter(operator_id=operator_object.id).order_by('sequence')
        info=[]
        input_num=0
        output_num=0
        for operator_parameter in operator_parameters:
            if operator_parameter.parameter_type=='input':
                input_num+=1
            elif operator_parameter.parameter_type=='output':
                output_num+=1
            node_parameter=(Node_parameter.objects.filter(node_id=node_object.id).filter(operator_parameter_id=operator_parameter.id))[0]
            info.append({
                'id':operator_parameter.id,'name':operator_parameter.name,'value':node_parameter.value,'description':operator_parameter.description,'parameter_type':operator_parameter.parameter_type,'export':node_parameter.export
            })
        opInformation={
            'id':operator_object.id,'name':operator_object.name,'info':info,'input_num':input_num,'output_num':output_num
        }
        node={
            'id':node_object.id,'pos_x':float(node_object.pos_x),'pos_y':float(node_object.pos_y),'taskID':node_object.task_ID,'type':node_object.node_type,'opInformation':opInformation,'node_location':node_object.node_location
        }
        nodes.append(node)
    lines=[]
    line_objects=DAG_line.objects.filter(App_id=appID)
    for line_object in line_objects:
        line={}
        from_node_circle_object=DAG_node_circle.objects.get(pk=line_object.from_node_circle_id)
        line['from_node_circle']={
            'node_circle':from_node_circle_object.node_circle,
            'pos_x':float(from_node_circle_object.pos_x),
            'pos_y':float(from_node_circle_object.pos_y),
            'task':DAG_node.objects.get(pk=from_node_circle_object.node_id).task_ID
        }
        to_node_circle_object=DAG_node_circle.objects.get(pk=line_object.to_node_circle_id)
        line['to_node_circle']={
            'node_circle':to_node_circle_object.node_circle,
            'pos_x':float(to_node_circle_object.pos_x),
            'pos_y':float(to_node_circle_object.pos_y),
            'task':DAG_node.objects.get(pk=to_node_circle_object.node_id).task_ID
        }
        lines.append(line)
    return nodes,lines

def check_no_incoming(incoming):
    q_no_incoming_indexs=Queue(maxsize=len(incoming))
    index=0
    for node in incoming:
        if node ==0:
            q_no_incoming_indexs.put(index)
        index+=1
    return q_no_incoming_indexs

def rename_inputs(dstFiles,preWaitIds):
    print(dstFiles)
    ret=[]
    index=0
    preWaitIds=preWaitIds.split()
    for preWaitId in preWaitIds:
        object=Task_node_wait.objects.get(pk=int(preWaitId))
        outputs=json.loads(object.outputs)
        i=0
        for out in outputs:
            if out['used']==0:
                outputs[i]['used']=1
                srcFile=out['filepath']
                break
            i+=1
        object.outputs=json.dumps(outputs)
        object.save()
        ret.append({
            'srcFile':srcFile,
            'dstFile':dstFiles[index]['filepath']
        })
        index+=1
    return json.dumps(ret)

def convert_mediaFile_to_workFile(filename,imgDir,node):
    info=node['opInformation']['info']
    for item in info:
        if item['parameter_type']=='input':
            file_name=item['value']
    rootFile=os.path.join(imgDir,file_name)
    return json.dumps([{'srcFile':filename,'dstFile':rootFile}])

def create_output(node):
    info=node['opInformation']['info']
    outputs=[]
    for item in info:
        if item['parameter_type']=='output':
            outputs.append(item['value'])
    dir=get_work_dir()
    for output in outputs:
        filename=os.path.join(dir,output)
        file = open(filename,'w')
        file.close()

def run_task(taskID,nodes,lines,input_file):
    task_object=Task.objects.get(pk=taskID)
    task_to_index_dict=dict()
    index_to_task_dict=dict()
    indexPreWaitIds=dict()
    incoming=[0]*len(nodes)
    index=0
    for node in nodes:
        task_to_index_dict[node['taskID']]=index
        index_to_task_dict[index]=node['taskID']
        indexPreWaitIds[index]=""
        index+=1
    for line in lines:
        incoming[task_to_index_dict[line['to_node_circle']['task']]]+=1
    q_no_incoming_indexs=check_no_incoming(incoming)
    flag=True
    while q_no_incoming_indexs.empty()==False :
        no_incoming_index=q_no_incoming_indexs.get()
        node=nodes[no_incoming_index]
        node_object=DAG_node.objects.get(pk=node['id'])
        operator_object=node_object.operator
        operator_distribute=(Operator_distribute.objects.filter(operator_id=operator_object.id))[0]
        container=operator_distribute.container
        container_object=Container.objects.get(pk=container.id)
        imgDir=container_object.imgDir
        parameter_values=[]
        input_values=[]
        output_values=[]
        info=node['opInformation']['info']
        task_dir=os.path.join(os.path.join(container_object.imgDir,str(task_object.id)),str(node_object.id))
        localInputDir=os.path.join(task_dir,'input')
        localOutputDir=os.path.join(task_dir,'output')
        for item in info:
            value=item['value']
            if item['parameter_type']=='output':
                v=os.path.join(localOutputDir,value)
                output_values.append({
                    'filepath':v,
                    'used':0
                })
                v=os.path.join(operator_object.outputDir,value)
                parameter_values.append(v)
            elif item['parameter_type']=='input':
                v=os.path.join(operator_object.inputDir,value)
                parameter_values.append(v)
                v=os.path.join(localInputDir,value)
                input_values.append({
                    'filepath':v,
                    'used':0
                })
        # print ('node',node['taskID'],'开始执行')
        # task_node_status_object.status='Run'
        # task_node_status_object.save()
        print(parameter_values)
        parameter=' '.join(parameter_values)
        inputs=json.dumps(input_values)
        outputs=json.dumps(output_values)
        preWaitIds=indexPreWaitIds[no_incoming_index]
        if flag:
            renameInputs=convert_mediaFile_to_workFile(input_file,localInputDir,node)
            flag=False
        else:
            renameInputs=rename_inputs(json.loads(inputs),preWaitIds)

        task_node_wait=Task_node_wait(
            parameters=parameter,
            inputs=inputs,
            outputs=outputs,
            status=0,
            ip=container_object.ip,
            port=container_object.port,
            localInputDir=localInputDir,
            localOutputDir=localOutputDir,
            imageInputDir=operator_object.inputDir,
            imageOutputDir=operator_object.outputDir,
            workFilename=operator_object.workFilename,
            containername=operator_distribute.containername,
            preWaitIds=preWaitIds,
            node_location=node_object.node_location,
            task=task_object,
            node=node_object,
            renameInputs=renameInputs
        )
        task_node_wait.save()
        for line in lines:
            print(line['from_node_circle']['task'])
            if not 'status' in line and line['from_node_circle']['task']==node['taskID']:
                line['status']=True
                to_node_taskID=line['to_node_circle']['task']
                to_node_index=task_to_index_dict[to_node_taskID]
                incoming[to_node_index]-=1
                indexPreWaitIds[to_node_index]=indexPreWaitIds[to_node_index]+" "+str(task_node_wait.id)
                if incoming[to_node_index]==0:
                    q_no_incoming_indexs.put(to_node_index)

    

def app_list(request):
    res=[]
    app_objects=App.objects.all()
    for app in app_objects:
        res.append({
            "id":app.id,
            "name":app.name
        })
    data = {'msg': '任务列表', "appList": res}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')

def create_app(request):
    name=request.POST['name']
    app=App()
    app.name=name
    app.save()
    data = {
            'msg': '创建成功',
            'id':app.id
        }
    return JsonResponse(data=data)
    #\r*+e/]turn redirect(reverse('app:file_info', args={file.id}))

def delete_app(request):
    try:
        id = int(request.POST['id'])
        app = App.objects.get(pk=id)
        if app != None:
            app.delete()
            data = {'msg': '删除成功', 'status': 0}
        else:
            data = {'msg': '删除失败', 'status': 1}
    except:
        data = {'msg': 'wrong', 'status': 1}
    return JsonResponse(data=data)

def create_operator(request):
    name=request.POST['name']
    file=request.FILES.get('file')
    description=request.POST['description']
    paramters=request.POST['paramters']
    inputDir=request.POST['inputDir']
    outputDir=request.POST['outputDir']
    workFilename=request.POST['workFilename']
    parameters=json.loads(paramters)
    filename=file.name
    imagename=filename.rsplit('.')[0]
    operator=Operator(
        name=name,
        file=file,
        description=description,
        filename=filename,
        imagename=imagename,
        inputDir=inputDir,
        outputDir=outputDir,
        workFilename=workFilename,
        loading=True
    )
    operator.save()
    sequence=0
    for paramter in parameters:
        paramter_object=Operator_parameter()
        paramter_object.operator=operator
        paramter_object.sequence=sequence
        paramter_object.name=paramter['name']
        paramter_object.parameter_type=paramter['type']
        paramter_object.description=paramter['description']
        paramter_object.save()
        sequence+=1

    containername="{0}_{1}".format(imagename,str(random.randint(0,2222)))
    container_object=Container.objects.all()[0]
    operator_distribute=Operator_distribute(
        operator=operator,
        container=container_object,
        containername=containername
    )
    operator_distribute.save()
    imagelocation=os.path.join(container_object.operatorDir,filename)
    #把file存到本地
    #save_file(dir,file.chunks())
    #新建容器
    distribute_wait=Distribute_wait(
        operator_distribute=operator_distribute,
        parameters='{0} {1} {2} {3} {4} {5}'.format(imagelocation,imagename,containername,container_object.imgDir,inputDir,outputDir),
        status=0,
        containername=containername,
        ip=container_object.ip,
        port=container_object.port,
        filename=filename,
        filelocation=os.path.join('operator',file.name),
        operatorDir=container_object.operatorDir
    )
    distribute_wait.save()
    data = {'msg': '新建算子成功', 'status':0}
    return JsonResponse(data=data)

def edit_operator_list(request):
    operator_objects=Operator.objects.all()
    ret=[]
    for object in operator_objects:
        ret.append({
            'id':object.id,
            'name':object.name,
            'description':object.description,
            'date':object.create_date,
            'loading':object.loading
        })
    data = {'msg': '算子列表', 'operatorList':ret}
    return JsonResponse(data=data)

def view_operator_list(request):
    operator_objects=Operator.objects.all()
    ret=[]
    for object in operator_objects:
        if object.loading==True:
            continue
        info=[]
        input_num=0
        output_num=0
        operator_parameters=Operator_parameter.objects.filter(operator_id=object.id)
        for parameter in operator_parameters:
            info.append({
                'id':parameter.id,
                'name':parameter.name,
                'description':parameter.description,
                'parameter_type':parameter.parameter_type
            })
            if parameter.parameter_type=="input":
                input_num+=1
            elif parameter.parameter_type=="output":
                output_num+=1
        operator={
            'name':object.name,
            'id':object.id,
            'info':info,
            'input_num':input_num,
            'output_num':output_num
        }
        ret.append(operator)
    data = {'msg': '任务列表', "operatorList": ret}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')


def save_app(request):
    appID=int(request.POST['appID'])
    app = App.objects.get(pk=appID)
    name=app.name
    app.delete()
    app=App(
        name=name
    )
    app.save()
    appID=app.id
    #解析node数据 存储入数据库
    nodes=request.POST.get("nodes")
    nodes=json.loads(nodes)
    for item in nodes:
        task_ID=item['taskID']
        print(item)
        node=DAG_node()      
        opInformation=item['opInformation']
        node.operator=Operator.objects.get(pk=opInformation['id'])
        node.task_ID=task_ID
        node.App=app
        node.pos_x=float(item['pos_x'])
        node.pos_y=float(item['pos_y'])
        node.node_location=item['node_location']
        node.save()
        for p in opInformation['info']:
            node_parameter=Node_parameter()
            node_parameter.node=node
            node_parameter.operator_parameter=Operator_parameter.objects.get(pk=p['id'])
            node_parameter.value=p['value']
            node_parameter.export=p['export']
            node_parameter.save()
    #修改线段
    lines=request.POST.get("lines")
    lines=json.loads(lines)
    for line in lines:
        from_node_circle=line['from_node_circle']
        to_node_circle=line['to_node_circle']
        circles=[from_node_circle,to_node_circle]
        for circle in circles:
            node=(DAG_node.objects.filter(App_id=appID).filter(task_ID=circle['task']))[0]
            circle_objects=DAG_node_circle.objects.filter(node_id=node.id).filter(node_circle=circle['node_circle'])
            if len(circle_objects) == 0:
                circle_object=DAG_node_circle()
                print(int(circle['node_circle']))
                circle_object.node_circle=int(circle['node_circle'])
                circle_object.node=node
                circle_object.pos_x=float(circle['pos_x'])
                circle_object.pos_y=float(circle['pos_y'])
                circle_object.save()
            circle_objects=DAG_node_circle.objects.filter(node_id=node.id).filter(node_circle=circle['node_circle'])
            circle_object=DAG_node_circle.objects.get(pk=circle_objects[0].id)
            circle_object.pos_x=float(circle['pos_x'])
            circle_object.pos_y=float(circle['pos_y'])
            circle_object.save()
        node=(DAG_node.objects.filter(App_id=appID).filter(task_ID=from_node_circle['task']))[0]
        from_node_circle_object=(DAG_node_circle.objects.filter(node_id=node.id).filter(node_circle=from_node_circle['node_circle']))[0]
        node=(DAG_node.objects.filter(App_id=appID).filter(task_ID=to_node_circle['task']))[0]
        to_node_circle_object=(DAG_node_circle.objects.filter(node_id=node.id).filter(node_circle=to_node_circle['node_circle']))[0]
        lines=DAG_line.objects.filter(from_node_circle_id=from_node_circle_object.id).filter(to_node_circle_id=to_node_circle_object.id)
        if len(lines)==0:
            line=DAG_line()
            line.from_node_circle=from_node_circle_object
            line.to_node_circle=to_node_circle_object
            line.App=app
            line.save()
    data = {'msg': '保存成功', 'status': 0}
    return JsonResponse(data=data)

def view_app(request):
    appID = int(request.GET['appID'])
    nodes,lines=get_DAG_info(appID)
    data = {'msg': '应用信息', 'nodes':nodes,'lines':lines}
    return JsonResponse(data=data)

def create_task(request):
    # info=[
    #     'Start','Pause','Run','End'
    # ]
    task=None
    try:
        appId=int(request.POST['id'])
        input=request.FILES.get('file')
        task = Task(
            app=App.objects.get(pk=appId),
            input=input,
            name = request.POST['name'],
            status='Start'
            )
        task.save()
    except:
        data = {
            'msg': '创建失败,应用名不可重复','stauts':1
        }
        return JsonResponse(data=data)
    node_objects=DAG_node.objects.filter(App_id=appId)
    for node_object in node_objects:
        node=DAG_node.objects.get(pk=node_object.id)
        operator_object=node.operator
        task_node_status=Task_node_status(
            task=task,
            node=node,
            status="Start",
            container=Container.objects.get(pk=1) 
        )
        task_node_status.save()
    nodes,lines=get_DAG_info(appId)
    input_location=os.path.join(os.path.join(settings.BASE_DIR,'media'),task.input.name)
    print(input_location)
    run_task(task.id,nodes,lines,input_location)
    data = {'msg': '创建成功', 'status':0}
    return JsonResponse(data=data)

def task_list(request):
    task_objects=Task.objects.all()
    taskList=[]
    for task_object in task_objects:
        taskList.append({
            'taskID':task_object.id,
            'taskName':task_object.name,
            'Status':task_object.status,
        })
    data = {
            'msg': '应用列表','taskList':taskList
        }
    return JsonResponse(data=data)

def view_task(request):
    taskID=int(request.GET['taskID'])
    task=Task.objects.get(pk=taskID)
    appId=task.app_id
    status=task.status
    nodes_objects=DAG_node.objects.filter(App_id=appId)
    nodes=[]
    for nodes_object in nodes_objects:
        operator_object=Operator.objects.get(pk=nodes_object.operator_id)
        task_node_status=(Task_node_status.objects.filter(task_id=taskID).filter(node_id=nodes_object.id))[0]
        nodes.append({
            'taskID':nodes_object.task_ID,
            'operatorID':operator_object.id,
            'operatorName':operator_object.name,
            'containerID':task_node_status.container.id,
            'server':task_node_status.server,
            'status':task_node_status.status
        })
    lines=[]
    line_objects=DAG_line.objects.filter(App_id=appId)
    for line_object in line_objects:
        from_operator=(DAG_node.objects.get(pk=(DAG_node_circle.objects.get(pk=line_object.from_node_circle_id)).node_id)).task_ID
        to_operator=(DAG_node.objects.get(pk=(DAG_node_circle.objects.get(pk=line_object.to_node_circle_id)).node_id)).task_ID
        lines.append({
            'from':from_operator,
            'to':to_operator
        })
    data = {'msg': '任务信息','nodes':nodes,'lines':lines,'status':status}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')

def detete_task(request):
    try:
        id = int(request.GET['id'])
        task = Task.objects.get(pk=id)
        if task != None:
            task.delete()
            data = {'msg': '删除成功', 'status': 0}
        else:
            data = {'msg': '删除失败,任务不存在', 'status': 1}
    except:
        data = {'msg': 'wrong', 'status': 1}
    return JsonResponse(data=data)

def container_list(request):
    container_objects=Container.objects.all()
    container_list=[]
    for container_object in container_objects:
        container_list.append({
            'containerID':container_object.id,
            'containerName':container_object.name
        })
    data = {'msg': '虚拟机列表','containerList':container_list}
    return JsonResponse(data=data)

def delete_operator(request):
    id=int(request.POST['id'])
    try:
        id = int(request.POST['id'])
        app = Operator.objects.get(pk=id)
        if app != None:
            app.delete()
            data = {'msg': '删除成功', 'status': 0}
        else:
            data = {'msg': '删除失败', 'status': 1}
    except:
        data = {'msg': 'wrong', 'status': 1}
    return JsonResponse(data=data)

def server_list(request):
    container_objects=Container.objects.all()
    server_list=[]
    for object in container_objects:
        server_list.append({
            'id':object.id,
            'name':object.name,
            'ip':object.ip,
            'port':object.port,
            'description':object.description,
            'CPU':object.CPU,
            'status':object.status,
            'capacity':object.capacity,
        })
    data = {'msg': '虚拟机列表','serverList':server_list}
    return JsonResponse(data=data)
    
def create_server(request):
    name=request.POST['name']
    ip=request.POST['ip']
    port=int(request.POST['port'])
    description=request.POST['description']
    CPU=int(request.POST['CPU'])
    capacity=request.POST['capacity']
    username=request.POST['username']
    password=request.POST['password']
    operatorDir=request.POST['operatorDir']
    imgDir=request.POST['imgDir']
    try:
        if ip in ['192.168.1.201','192.168.1.202','192.168.1.203','192.168.1.204','192.168.1.205']:
            container=Container(
            name=name,
            ip=ip,
            port=port,
            description=description,
            CPU=CPU,
            capacity=capacity,
            username=username,
            password=password,
            operatorDir=operatorDir,
            imgDir=imgDir,
            status="正常",
            busy=False
        )
            container.save()
            data = {'msg': '新建成功', 'status': 0}
        else:
            data = {'msg': '该连接不存在', 'status': 1}
    except:
        data = {'msg': '新建失败,请检查参数设置', 'status': 1}
    return JsonResponse(data=data)

def delete_server(request):
    id=int(request.POST['id'])
    try:
        container = Container.objects.get(pk=id)
        if container != None:
            container.delete()
            data = {'msg': '删除成功', 'status': 0}
        else:
            data = {'msg': '删除失败', 'status': 1}
    except:
        data = {'msg': 'wrong', 'status': 1}
    return JsonResponse(data=data)

def get_work_output_img(request):
    file=request.FILES.get('file')
    name=request.POST['name']
    save_file(os.path.join(get_work_out_dir(),name),file.chunks())
    data = {'msg': 'success', 'status': 0}
    return JsonResponse(data=data)

def get_task_output_img(request):
    taskID=int(request.GET['taskID'])
    task_output_objects=Task_output.objects.filter(task_id=taskID)
    imgList=[]
    for task_output_object in task_output_objects:
        imgList.append({
            'name':task_output_object.name,
            'url':'{0}/{1}'.format('media/task_img/output',task_output_object.file_location)

        })
    data = {'msg': '输出列表', "imgList": imgList}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')

def get_wait_node_by_task(request):
    taskID=int(request.GET['taskID'])
    objects=Task_node_wait.objects.filter(task_id=taskID)
    task_node_waits=[]
    for object in objects:
        task_node_waits.append({
            'id':object.id,
            'parameters':object.parameters,
            'status':object.status,
            'localInputDir':object.localInputDir,
            'localOutputDir':object.localOutputDir,
            'imageInputDir':object.imageInputDir,
            'imageOutputDir':object.imageOutputDir,
            'inputs':object.inputs,
            'outputs':object.outputs,
            'ip':object.ip,
            'port':object.port,
            'workFilename':object.workFilename,
            'containername':object.containername,
            'preWaitIds':object.preWaitIds,
            'node_location':object.node_location,
            'renameInputs':object.renameInputs
        })

    data = {'msg': '任务执行列表', "task_node_waits": task_node_waits}
    return HttpResponse(json.dumps(data, cls=DateEncoder), content_type='application/json')
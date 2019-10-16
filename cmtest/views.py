from django.shortcuts import render

from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import os
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cmtest.models import ProjectName, Files
from django.db.models import Q
# Create your views here.
def login_view(request):
    #request 包含用户提交的所有信息
    if request.method=='POST':
        user=request.POST.get("username",None)
        pwd=request.POST.get("pwd",None)
        # 验证用户
        user=authenticate(username=user, password=pwd)
        if user is not None:
            login(request, user)
            # 跳转到
            print("redirecting")
            return redirect("/index/index")
        else:
            print("error msg")
            return render(request,'login.html',{"error_msg":"密码错误"})
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/index/login')

@login_required
def change_pwd(request):
    username=request.user.username
    if request.method=='POST':
        userid=request.user.id
        pwd=request.POST.get("pwd",None)
        user_c=User.objects.get(id=userid)
        if user_c.check_password(pwd):
            print("PWD OK")
            pwd1=request.POST.get("pwd1",None)
            pwd2=request.POST.get("pwd2",None)
            print(pwd1,pwd2)
            if pwd1 != pwd2:
                print("两次密码不一致")
                return render(request,'change_pwd.html',{"error_msg":"两次密码不一致","username":username})
            else:
                user_c.set_password(pwd1)
                user_c.save()
                return render(request,'change_pwd.html',{"error_msg":"修改成功","username":username})
        else:
            return render(request,'change_pwd.html',{"error_msg":"原密码错误","username":username})

        
    if request.method=='GET':
        return render(request,'change_pwd.html',{"error_msg":"","username":username})

@login_required
def fileManager(request):
    username=request.user.username
    userid=request.user.id
    # 判断当前用户是否有上传权限的项目名
    projects=ProjectName.objects.all()
    if userid not in [i.author.id for i in projects]:# 
        return redirect("/index/index")
    # 判断当前用户是否为管理员
    group_manager =  Group.objects.get(name="manager")
    if group_manager in request.user.groups.all():
        proId=request.GET.get("pid",None)
        if not proId:
            files=Files.objects.filter(author=userid)
            return render(request,"File_manager.html",{"username":username,"files":files})
        else:
            files=Files.objects.filter(project=proId)
            return render(request,"File_manager_forManager.html",{"username":username,"files":files})
    else:
        files=Files.objects.filter(author=userid)
        return render(request,"File_manager.html",{"username":username,"files":files})

@login_required
def delete_file(request):
    userid=request.user.id
    fid   =request.GET.get("fid",None)
    f     =Files.objects.get(id=fid)
    # todo 检查此文件是否属于当前用户
    f.delete() #从数据库中删除 
    # todo 从文件中删除
    save_path=f.save_path
    try:
        os.remove(save_path)
        print("删除成功")
    except OSError as error:
        print("删除失败",error)
        return redirect("/index/fileManager/?pid="+str(f.project.id))

    return redirect("/index/fileManager/?pid="+str(f.project.id))

@login_required
def fileUploader(request):
    userid=request.user.id
    user = User.objects.get(id=userid)
    #获取当前用户的project
    project=ProjectName.objects.filter(author=user).first()

    # print(request.method)
    if request.method=="POST":
        filename = request.FILES.get('file',None)
        if filename==None:
            return redirect("/index/fileManager")
        # print(filename)
        f=request.FILES["file"]
        path_store="static/uploads/"+str(filename)
        with open(path_store, 'wb+') as fi:
            for chunk in f.chunks():
                fi.write(chunk)
        f = Files(name=filename,save_path=path_store, info_status='uploaded',project=project,author=user)
        f.save()
    return redirect("/index/fileManager")

@login_required
def index(request):
    username=request.user.username
    userid=request.user.id
    # 获取所有的管理员
    # 查看当前用户所属于的用户组 是否是 manager
    group_manager =  Group.objects.get(name="manager")

    projects=ProjectName.objects.filter()
    files=Files.objects.filter(id=1) # 公用文件
    for p in projects:
        usr=p.author
        if group_manager in usr.groups.all():
            # 如果 项目是管理员项目
            p.isShare=1
            # 获取项目中的所有文件
            files_i=Files.objects.filter(project=p) # 公用文件
            files=files.union(files_i)
        else:
            p.isShare=0
    
    #当前用户的project
    myProject=ProjectName.objects.filter(author=userid).first() 
    # 如果当前用户是管理员
    if group_manager in request.user.groups.all():
        isManager=1
    else:
        isManager=0

    return render(request,"index.html", 
        {"username":username,"projects":projects,"myProject":myProject,"files":files,"isManager":isManager})


from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
#模型
from UserManager import models

def UserManager(request):
    #创建数据
    # models.UserInfo.objects.create(username="root",password="694595504",project_name="root",role=0)
    # obj=models.UserInfo(username="lsf",password="694595504",project_name="某项目",role=2)
    # obj.save()
    users=models.UserInfo.objects.all()
    # print(users) ## result,querySet =>Djiango=>[]
    return render(request,"user_manager.html",{"users":users})


def UserManager_add(request):
    if request.method=='POST':
        user=request.POST.get("username",None)
        pwd=request.POST.get("pwd",None)
        role=request.POST.get("role",None)
        project_name=request.POST.get("project_name",None)
        models.UserInfo.objects.create(username=user,password=pwd,role=role,project_name=project_name)
        
    return redirect("/userManager/userManager/")

def UserManager_del(request):
    if request.method=='GET':
        id=request.GET.get("id",None)
        models.UserInfo.objects.filter(id=id).delete()
    return redirect("/userManager/userManager/")
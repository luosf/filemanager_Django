from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# 项目名表
class ProjectName(models.Model):
    name  =models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

# 文件表
class Files(models.Model):
    name       =models.CharField(max_length=150)
    time_upload=models.DateTimeField('create time',default=timezone.now)
    save_path  =models.CharField(max_length=450)
    info_status=models.CharField(max_length=350)
    project    =models.ForeignKey(ProjectName,on_delete=models.CASCADE)
    author     =models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name




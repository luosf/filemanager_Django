from django.contrib import admin
from .models import ProjectName, Files

class FilesAdmin(admin.ModelAdmin):
    list_display=['name','time_upload','save_path','info_status','project','author']


# Register your models here
admin.site.register(ProjectName)
admin.site.register(Files,FilesAdmin)
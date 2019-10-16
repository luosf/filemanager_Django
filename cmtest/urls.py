from django.urls import path
from cmtest import views as v1
urlpatterns = [
    path('login/',v1.login_view),
    path('logout/',v1.logout_view),
    path('change_pwd/',v1.change_pwd),
    path('index/',v1.index),
    path('fileManager/',v1.fileManager),
    path('fileUploader/',v1.fileUploader),
    path('delete/',v1.delete_file),
]

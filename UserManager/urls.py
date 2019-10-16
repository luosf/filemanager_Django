from django.urls import path
from UserManager import views as v2
urlpatterns = [
    path('userManager/',v2.UserManager),
    path('userManager_add/',v2.UserManager_add),
    path('userManager_del/',v2.UserManager_del),
]

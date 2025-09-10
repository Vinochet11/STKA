from django.urls import path
from .views import (user_list,user_register,plans_list,plans_register,index,panel)

urlpatterns=[
    path('',index, name='index'),
    path('panel',panel,name='panel'),
    #ususarios
    path('user/',user_list,name='user_list'),
    path('user/new/',user_register,name='user_register'),
    #plans
    path('plans/',plans_list,name='plans_list'),
    path('plans/new/',plans_register,name='plans_register')
]
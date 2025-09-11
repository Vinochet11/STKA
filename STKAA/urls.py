from django.urls import path
from .views import (index,user_list, user_register,plans_list, plans_register,activities_list, activities_register,sessions_list, sessions_register,bookings_list,)

urlpatterns=[
    path('',index, name='index'),
    
    #ususarios
    path('user/',user_list,name='user_list'),
    path('user/new/',user_register,name='user_register'),
    #plans
    path('plans/',plans_list,name='plans_list'),
    path('plans/new/',plans_register,name='plans_register'),
    
    path('activities/',activities_list,name='activities_list'),
    path('activities/new/',activities_register,name='activities_register'),
    path('sessions/',sessions_list,name='sessions_list'),
    path('sessions/new/',sessions_register,name='sessions_register'),
    path('bookings/',bookings_list,name='bookings_list'),
]



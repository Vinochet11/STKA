from django.urls import path
from .views import (
    index,
    user_list, user_register,
    plans_list, plans_register, plans_edit, plans_delete,
    activities_list, activities_register, activities_edit, activities_delete,
    sessions_list, sessions_register, bookings_list, 
)

urlpatterns = [
    path('', index, name='index'),



    path('user/', user_list, name='user_list'),
    path('user/new/', user_register, name='user_register'),


    path('plans/', plans_list, name='plans_list'),
    path('plans/new/', plans_register, name='plans_register'),
    path('plans/<int:plan_id>/edit/', plans_edit, name='plans_edit'),
    path('plans/<int:plan_id>/delete/', plans_delete, name='plans_delete'),

    path('activities/', activities_list, name='activities_list'),
    path('activities/new/', activities_register, name='activities_register'),
    path('activities/<int:activity_id>/edit/', activities_edit, name='activities_edit'),
    path('activities/<int:activity_id>/delete/', activities_delete, name='activities_delete'),

    path('sessions/', sessions_list, name='sessions_list'),
    path('sessions/new/', sessions_register, name='sessions_register'),
    path('bookings/', bookings_list, name='bookings_list'),
]

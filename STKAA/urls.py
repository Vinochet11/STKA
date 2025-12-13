from django.urls import path
from .views import (
    index,
    user_list, user_register,
    planes_list, cr_plan, plans_editar, plans_br,
    activities_list, activities_register, activities_edit, activities_delete,
    sessions_list, sessions_register, sessions_edit, sessions_delete, session_estudiante,
    bookings_list, booking_register, booking_edit, booking_delete,
    login_view, logout_view,
    panel
)

urlpatterns = [
    path('', index, name='index'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('user/', user_list, name='user_list'),
    path('user/new/', user_register, name='user_register'),

    path('plans/', planes_list, name='plans_list'),
    path('plans/new/', cr_plan, name='cr_plan'),
    path('plans/<int:plan_id>/edit/', plans_editar, name='plans_edit'),
    path('plans/<int:plan_id>/delete/', plans_br, name='plans_br'),

    path('activities/', activities_list, name='activities_list'),
    path('activities/new/', activities_register, name='activities_register'),
    path('activities/<int:activity_id>/edit/', activities_edit, name='activities_edit'),
    path('activities/<int:activity_id>/delete/', activities_delete, name='activities_delete'),

    path('sessions/', sessions_list, name='sessions_list'),
    path('sessions/new/', sessions_register, name='sessions_register'),
    path('sessions/<int:session_id>/edit/', sessions_edit, name='sessions_edit'),
    path('sessions/<int:session_id>/delete/', sessions_delete, name='sessions_delete'),
    path('sessions/<int:session_id>/estudiantes/', session_estudiante, name='session_estudiante'),

    path('bookings/', bookings_list, name='bookings_list'),
    path('bookings/new/', booking_register, name='booking_register'),
    path('bookings/<int:booking_id>/edit/', booking_edit, name='booking_edit'),
    path('bookings/<int:booking_id>/delete/', booking_delete, name='booking_delete'),

    path('panel/', panel, name='panel'),
]

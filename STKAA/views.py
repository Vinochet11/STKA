from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

USUARIOS=[
    
    {"id":1,"name":"Jose","Plan_mensual":1,"email":"test@test.cl","rol":"Admin","status":"Activo"},
    {"id":2,"name":"Javier","Plan_mensual":2,"email":"test@mail.com","rol":"user","status":"Inactivo"}

]
PLANES = [

     {"id": 1, "name_plan": "basico",   "mounthly_creditos": 100, "is_unlimited": False},
    {"id": 2, "name_plan": "avanzado", "mounthly_creditos": 300, "is_unlimited": False},
    {"id": 3, "name_plan": "premium",  "mounthly_creditos": None, "is_unlimited": True},

]

def index(request):
    return render(request,'index.html')

@login_required
def panel(request):
    return render(request,'STKAA/panel.html')


#usuarios
def user_list(request):
    return render(request,'user_list.html',{"users":USUARIOS})

def user_register(request):
    return render(request,'user_form.html')


#planes

def plans_list(request):
    return render(request,'plans_list.html',{"Plans":PLANES})
def plans_register(request):
    return render(request,'plans_forms.html')
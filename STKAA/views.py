from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

USUARIOS=[
    
    {"id":1,"name":"Jose","Plan_mensual":1,"email":"test@test.cl","rol":"Admin","status":"Activo"},
    {"id":2,"name":"Javier","Plan_mensual":2,"email":"test@mail.com","rol":"user","status":"Inactivo"}

]
PLANES = [
    {"id": 1, "name_plan": "basico",   "clases_mensuales": 15, "is_unlimited": False},
    {"id": 2, "name_plan": "avanzado", "clases_mensuales": 30, "is_unlimited": False},
    {"id": 3, "name_plan": "premium",  "clases_mensuales": None, "is_unlimited": True},
]

PLANxID={p["id"]:p for p in PLANES} #


SESSIONS=[

    {"id":1,"activity_id":1,"start_class":"10/09/2025 21:00", "end_class":"10/09/2025 22:00", "status":"terminada" },
    {"id":2,"activity_id":2,"start_class":"10/09/2025 11:00 ","end_class":"10/09/2025 12:00","status":"terminada"},
    {"id":3,"activity_id":3,"start_class":"11/09/2025 16:00","end_class":"11/09/2025 17:00","status":"cancelada"}
    
]

BOOKING=[

    {"id":1,"user_id":2,"status":"cancelada"},
    {"id":2,"user_id":1,"status":"asistire"}

]

ACTIVIDADES =[

    {"id":1,"name":"boxeo"},
    {"id":2,"name":"kickboxing"},
    {"id":3,"name":"gimnasia funcional"},

]

ACTIVIDAD_MAP={a["id"]:a["name"]for a in ACTIVIDADES}


def index(request):
    return render(request,'index.html')

@staff_member_required
def user_list(request):
    users_enriched = []
    for u in USUARIOS:
        pid = u.get("Plan_mensual")  
        plan = PLANxID.get(pid)
        users_enriched.append({
            **u,
            "plan_nombre": plan["name_plan"] if plan else "—",
            "plan_clases": (
                plan["clases_mensuales"]
                if plan and plan["clases_mensuales"] is not None
                else "—"
            ),
            "plan_ilimitado": plan["is_unlimited"] if plan else False,
        })
    return render(request, 'user_list.html', {"users": users_enriched})

@staff_member_required
def user_register(request):
    return render(request,'user_form.html')


@login_required
def plans_list(request):
    return render(request,'plans_list.html',{"plans":PLANES})

@staff_member_required
def plans_register(request):
    return render(request,'plans_forms.html')


@login_required
def activities_list(request):
    return render(request,'activities_list.html',{"activities":ACTIVIDADES})

@staff_member_required
def activities_register(request):
    return render(request,'activities_forms.html')


@login_required
def sessions_list(request):
   
    sessions_enriched = [
        {**s, "activity_name": ACTIVIDAD_MAP.get(s["activity_id"], "—")}
        for s in SESSIONS
    ]
    return render(
        request,
        'sessions_list.html',
        {
            "sessions": sessions_enriched,
            "activity_map": ACTIVIDAD_MAP,  # opcional ya
        }
    )

@staff_member_required
def sessions_register(request):
    return render(request,'sessions_form.html') 


@login_required
def bookings_list(request):
    return render(request,'bookings_list.html',{"bookings":BOOKING})


@login_required
def bookings_list(request):
    bookings_enriched = []
    for b in BOOKING:
        user_name = USER_NAME_MAP.get(b.get("user_id"), "—")

        session = SESSION_MAP.get(b.get("session_id")) if b.get("session_id") else None
        activity_name = ACTIVIDAD_MAP.get(session["activity_id"]) if session else "—"
        start_class   = session["start_class"] if session else "—"

        bookings_enriched.append({
            **b,
            "user_name": user_name,
            "activity_name": activity_name,
            "start_class": start_class,
        })

    return render(request, 'bookings_list.html', {"bookings": bookings_enriched})




USER_NAME_MAP = {u["id"]: u["name"] for u in USUARIOS}
SESSION_MAP   = {s["id"]: s for s in SESSIONS} 


# STKAA/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Actividad

# --- MODELOS / FORMS ---
from STKAA.models import Plan
from STKAA.forms import anadirPlan

from .models import Actividad
from STKAA.forms import ActividadForm

# ------------------ DATOS EN MEMORIA (DEMO) ------------------
USUARIOS = [
    {"id": 1, "name": "Jose",   "Plan_mensual": 1, "email": "test@test.cl",  "rol": "Admin", "status": "Activo"},
    {"id": 2, "name": "Javier", "Plan_mensual": 2, "email": "test@mail.com", "rol": "user",  "status": "Inactivo"},
]

SESSIONS = [
    {"id": 1, "activity_id": 1, "start_class": "10/09/2025 21:00", "end_class": "10/09/2025 22:00", "status": "terminada"},
    {"id": 2, "activity_id": 2, "start_class": "10/09/2025 11:00", "end_class": "10/09/2025 12:00", "status": "terminada"},
    {"id": 3, "activity_id": 3, "start_class": "11/09/2025 16:00", "end_class": "11/09/2025 17:00", "status": "cancelada"},
]

BOOKING = [
    {"id": 1, "user_id": 2, "session_id": 1, "status": "cancelada"},
    {"id": 2, "user_id": 1, "session_id": 2, "status": "asistire"},
]

ACTIVIDADES = [
    {"id": 1, "name": "boxeo"},
    {"id": 2, "name": "kickboxing"},
    {"id": 3, "name": "gimnasia funcional"},
]

# ------------------ HELPERS ------------------
def get_next_id(items) -> int:
    return (max([it["id"] for it in items], default=0) + 1)

def actividad_map():
    return {a["id"]: a["name"] for a in ACTIVIDADES}

def user_name_map():
    return {u["id"]: u["name"] for u in USUARIOS}

def session_map():
    return {s["id"]: s for s in SESSIONS}

# ------------------ VISTAS BASE ------------------
def index(request):
    return render(request, 'index.html')

@staff_member_required
def user_list(request):
    # Nota: ya no se enriquece con PLANES (lista en memoria) para evitar inconsistencias.
    return render(request, 'user_list.html', {"users": USUARIOS})

@staff_member_required
def user_register(request):
    return render(request, 'user_form.html')

# ------------------ PLANES (DB) ------------------
@staff_member_required
def cr_plan(request):
    if request.method == "POST":
        form = anadirPlan(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plans_list")
        # Si no es válido, re-render con errores
        return render(request, "plans_forms.html", {"form": form, "mode": "create"})
    else:
        form = anadirPlan()
    return render(request, "plans_forms.html", {"form": form, "mode": "create"})

# Quita @login_required si quieres que cualquiera lo vea
def planes_list(request):
    planes = Plan.objects.all().order_by("id")
    return render(request, "plans_list.html", {"plans": planes})

@staff_member_required
def plans_editar(request, plan_id: int):
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == "POST":
        form = anadirPlan(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plans_list')
    else:
        form = anadirPlan(instance=plan)
    return render(request, 'plans_forms.html', {"form": form, "mode": "edit"})

@staff_member_required
def plans_br(request, plan_id: int):
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == "POST":
        plan.delete()
        return redirect('plans_list')
    # Si alguien entra por GET, lo mandamos a la lista
    return redirect('plans_list')

# --- Activities ---
#@login_required
def activities_list(request):
    acts = Actividad.objects.order_by("id")
    return render(request, "activities_list.html", {"activities": acts})

@staff_member_required
def activities_register(request):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("activities_list")
    else:
        form = ActividadForm()
    return render(request, "activities_forms.html", {"form": form, "mode": "create"})

@staff_member_required
def activities_edit(request, activity_id):
    act = get_object_or_404(Actividad, pk=activity_id)
    if request.method == "POST":
        form = ActividadForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            return redirect("activities_list")
    else:
        form = ActividadForm(instance=act)
    return render(request, "activities_forms.html", {"form": form, "mode": "edit"})

@staff_member_required
def activities_delete(request, activity_id):
    act = get_object_or_404(Actividad, pk=activity_id)
    if request.method == "POST":
        act.delete()
        return redirect("activities_list")
    return redirect("activities_list")













# ------------------ SESIONES / RESERVAS (DEMO EN MEMORIA) ------------------
#@login_required
def sessions_list(request):
    amap = actividad_map()
    sessions_enriched = [{**s, "activity_name": amap.get(s["activity_id"], "—")} for s in SESSIONS]
    return render(request, 'sessions_list.html', {"sessions": sessions_enriched, "activity_map": amap})

@staff_member_required
def sessions_register(request):
    return render(request, 'sessions_form.html')

@login_required
def bookings_list(request):
    uname = user_name_map()
    smap  = session_map()
    amap  = actividad_map()

    bookings_enriched = []
    for b in BOOKING:
        session = smap.get(b.get("session_id"))
        bookings_enriched.append({
            **b,
            "user_name":     uname.get(b.get("user_id"), "—"),
            "activity_name": amap.get(session["activity_id"]) if session else "—",
            "start_class":   session["start_class"] if session else "—",
        })
    return render(request, 'bookings_list.html', {"bookings": bookings_enriched})

@login_required
def panel(request):
    return render(request, 'STKAA/panel.html')



def index(request):
    # KPIs sencillos
    kpi_planes = Plan.objects.count()
    kpi_actividades = len(ACTIVIDADES)
    kpi_clases = len(SESSIONS)

    # “Próximas” clases demo (las primeras 5 de tu lista)
    amap = actividad_map()   # ya definida en tu views.py
    sesiones = [
        {
            **s,
            "activity_name": amap.get(s["activity_id"], "—")
        }
        for s in SESSIONS[:5]
    ]

    context = {
        "kpi_planes": kpi_planes,
        "kpi_actividades": kpi_actividades,
        "kpi_clases": kpi_clases,
        "sesiones": sesiones,
        "actividades": ACTIVIDADES[:8],  # muestra algunas
    }
    return render(request, "index.html", context)
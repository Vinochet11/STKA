# STKAA/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Modelos
from STKAA.models import Plan, Actividad, Clase,Usuario

# Forms
from STKAA.forms import anadirPlan, ActividadForm, ClaseForm,UsuarioForm


# ------------------ DATOS DEMO (SOLO PARA USUARIOS/BOOKINGS) ------------------
USUARIOS = [
    {"id": 1, "name": "Jose",   "Plan_mensual": 1, "email": "test@test.cl",  "rol": "Admin", "status": "Activo"},
    {"id": 2, "name": "Javier", "Plan_mensual": 2, "email": "test@mail.com", "rol": "user",  "status": "Inactivo"},
]

BOOKING = [
    {"id": 1, "user_id": 2, "session_id": 1, "status": "cancelada"},
    {"id": 2, "user_id": 1, "session_id": 2, "status": "asistire"},
]


# ------------------ HELPERS ------------------
def user_name_map():
    return {u["id"]: u["name"] for u in USUARIOS}

def session_map_from_db():
    """
    Mapa de Clases (BD) por id para enriquecer las reservas demo.
    """
    out = {}
    for c in Clase.objects.all():
        out[c.id] = {
            "id": c.id,
            "activity_name": c.actividad,
            "start_class": c.inicio,
            "end_class": c.termino,
            "status": c.estado,
        }
    return out


# ------------------ HOME / DASHBOARD ------------------
def index(request):
    # KPIs desde la BD
    kpi_planes = Plan.objects.count()
    kpi_actividades = Actividad.objects.count()
    kpi_clases = Clase.objects.count()

    
    sesiones = [
        {
            "activity_name": c.actividad,
            "start_class": c.inicio,
            "end_class": c.termino,
            "status": c.estado,
        }
        for c in Clase.objects.order_by("inicio")[:5]
    ]

    
    actividades = Actividad.objects.order_by("id")[:8]

    context = {
        "kpi_planes": kpi_planes,
        "kpi_actividades": kpi_actividades,
        "kpi_clases": kpi_clases,
        "sesiones": sesiones,        # el template index.html usa: activity_name, start_class, end_class, status
        "actividades": actividades,  # el template muestra a.nombre
    }
    return render(request, "index.html", context)


# ------------------ USUARIOS  ------------------
@staff_member_required
def user_list(request):
    users=Usuario.objects.select_related("plan").all().order_by("id")
    return render(request,'user_list.html',{"users":users})

@staff_member_required
def user_register(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
        # <-- DEBUG: imprime errores en consola
        print("UsuarioForm errors:", form.errors.as_json())
    else:
        form = UsuarioForm()
    return render(request, "user_form.html", {"form": form})


# ------------------ PLANES (BD) ------------------
@staff_member_required
def cr_plan(request):
    if request.method == "POST":
        form = anadirPlan(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plans_list")
        return render(request, "plans_forms.html", {"form": form, "mode": "create"})
    else:
        form = anadirPlan()
    return render(request, "plans_forms.html", {"form": form, "mode": "create"})

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
    return redirect('plans_list')


# ------------------ ACTIVIDADES (BD) ------------------
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


# ------------------ CLASES (BD, sin FK) ------------------



def sessions_list(request):
    clases=Clase.objects.select_related("actividad").order_by("inicio")
    #clases = Clase.objects.order_by("inicio")
    return render(request, "sessions_list.html", {"sessions": clases})

def _actividad_options():
    nombres = list(Actividad.objects.order_by("nombre").values_list("nombre", flat=True))
   

@staff_member_required
def sessions_register(request):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sessions_list")
    else:
        form = ClaseForm()
    return render(
        request,
        "sessions_form.html",
        {"form": form, "mode": "create"},
    )

@staff_member_required
def sessions_edit(request, session_id: int):
    clase = get_object_or_404(Clase, pk=session_id)
    if request.method == "POST":
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            return redirect("sessions_list")
    else:
        form = ClaseForm(instance=clase)
    return render(
        request,
        "sessions_form.html",
        {"form": form, "mode": "edit"},
    )

@staff_member_required
def sessions_delete(request, session_id: int):
    clase = get_object_or_404(Clase, pk=session_id)
    if request.method == "POST":
        clase.delete()
        return redirect("sessions_list")
    return redirect("sessions_list")


# ------------------ BOOKINGS  ------------------
@login_required
def bookings_list(request):
    uname = user_name_map()
    smap  = session_map_from_db()  # ahora desde BD

    bookings_enriched = []
    for b in BOOKING:
        session = smap.get(b.get("session_id"))
        bookings_enriched.append({
            **b,
            "user_name":     uname.get(b.get("user_id"), "—"),
            "activity_name": session["activity_name"] if session else "—",
            "start_class":   session["start_class"]   if session else "—",
        })
    return render(request, 'bookings_list.html', {"bookings": bookings_enriched})


# ------------------ PANEL ------------------
@login_required
def panel(request):
    return render(request, 'STKAA/panel.html')
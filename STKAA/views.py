from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# ------------------ DATOS EN MEMORIA ------------------

USUARIOS = [
    {"id": 1, "name": "Jose",   "Plan_mensual": 1, "email": "test@test.cl",  "rol": "Admin", "status": "Activo"},
    {"id": 2, "name": "Javier", "Plan_mensual": 2, "email": "test@mail.com", "rol": "user",  "status": "Inactivo"},
]

PLANES = [
    {"id": 1, "name_plan": "basico",   "clases_mensuales": 15,  "is_unlimited": False},
    {"id": 2, "name_plan": "avanzado", "clases_mensuales": 30,  "is_unlimited": False},
    {"id": 3, "name_plan": "premium",  "clases_mensuales": None,"is_unlimited": True},
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



# aqui comienza la configuracion de las views

def index(request):
    return render(request, 'index.html')

#
@staff_member_required
def user_list(request):
    plan_by_id = {p["id"]: p for p in PLANES}  
    users_enriched = []
    for u in USUARIOS:
        pid = u.get("Plan_mensual")
        plan = plan_by_id.get(pid)
        users_enriched.append({
            **u,
            "plan_nombre":   plan["name_plan"] if plan else "—",
            "plan_clases":   (plan["clases_mensuales"] if plan and plan["clases_mensuales"] is not None else "—"),
            "plan_ilimitado": plan["is_unlimited"] if plan else False,
        })
    return render(request, 'user_list.html', {"users": users_enriched})

@staff_member_required
def user_register(request):
    return render(request, 'user_form.html')

@login_required
def plans_list(request):
    return render(request, 'plans_list.html', {"plans": PLANES})

@staff_member_required
def plans_register(request):
    if request.method == "POST":
        name = (request.POST.get("name_plan") or "").strip()
        ilim = (request.POST.get("is_unlimited") == "1")  
        raw  = request.POST.get("clases_mensuales")
        clases = None
        if not ilim and raw:
            try:
                clases = int(raw)
            except ValueError:
                clases = None

        if not name:
            return render(request, 'plans_forms.html', {
                "error": "El nombre es obligatorio.",
                "plan": {"name_plan": name, "clases_mensuales": clases, "is_unlimited": ilim},
                "mode": "create",
            })

        PLANES.append({
            "id": next_id("plan"),
            "name_plan": name,
            "clases_mensuales": clases,
            "is_unlimited": ilim,
        })
        return redirect('plans_list')

    return render(request, 'plans_forms.html', {"mode": "create"})

@staff_member_required
def plans_edit(request, plan_id: int):
    plan = find_by_id(PLANES, plan_id)
    if not plan:
        raise Http404("Plan no existe")

    if request.method == "POST":
        name = (request.POST.get("name_plan") or "").strip()
        ilim = (request.POST.get("is_unlimited") == "1")
        raw  = request.POST.get("clases_mensuales")
        clases = None
        if not ilim and raw:
            try:
                clases = int(raw)
            except ValueError:
                clases = None

        if not name:
            return render(request, 'plans_forms.html', {
                "error": "El nombre es obligatorio.",
                "plan": {"id": plan_id, "name_plan": name, "clases_mensuales": clases, "is_unlimited": ilim},
                "mode": "edit",
            })

        plan.update({
            "name_plan": name,
            "clases_mensuales": clases,
            "is_unlimited": ilim,
        })
        return redirect('plans_list')

    return render(request, 'plans_forms.html', {"plan": plan, "mode": "edit"})

@staff_member_required
def plans_delete(request, plan_id: int):
    if request.method != "POST":
        raise Http404()
    remove_by_id(PLANES, plan_id)
    return redirect('plans_list')


@login_required
def activities_list(request):
    return render(request, 'activities_list.html', {"activities": ACTIVIDADES})

@staff_member_required
def activities_register(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if not name:
            return render(request, 'activities_form.html', {
                "error": "El nombre es obligatorio.",
                "activity": {"name": name},
                "mode": "create",
            })
        ACTIVIDADES.append({"id": next_id("act"), "name": name})
        return redirect('activities_list')

    return render(request, 'activities_forms.html', {"mode": "create"})

@staff_member_required
def activities_edit(request, activity_id: int):
    act = find_by_id(ACTIVIDADES, activity_id)
    if not act:
        raise Http404("Actividad no existe")

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if not name:
            return render(request, 'activities_form.html', {
                "error": "El nombre es obligatorio.",
                "activity": {"id": activity_id, "name": name},
                "mode": "edit",
            })
        act.update({"name": name})
        return redirect('activities_list')

    return render(request, 'activities_form.html', {"activity": act, "mode": "edit"})

@staff_member_required
def activities_delete(request, activity_id: int):
    if request.method != "POST":
        raise Http404()
    remove_by_id(ACTIVIDADES, activity_id)
    return redirect('activities_list')


@login_required
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


# Mapas auxiliares (se recalculan cuando hace falta)
def actividad_map():
    return {a["id"]: a["name"] for a in ACTIVIDADES}

def user_name_map():
    return {u["id"]: u["name"] for u in USUARIOS}

def session_map():
    return {s["id"]: s for s in SESSIONS}













# ------------------ HELPERS CRUD ------------------

NEXT_IDS = {
    "plan": max([p["id"] for p in PLANES] or [0]) + 1,
    "act":  max([a["id"] for a in ACTIVIDADES] or [0]) + 1,
}

def next_id(kind: str) -> int:
    nid = NEXT_IDS[kind]
    NEXT_IDS[kind] += 1
    return nid

def find_by_id(items, id_):
    for it in items:
        if it["id"] == id_:
            return it
    return None

def remove_by_id(items, id_) -> bool:
    for i, it in enumerate(items):
        if it["id"] == id_:
            del items[i]
            return True
    return False
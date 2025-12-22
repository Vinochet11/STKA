from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

import requests

from .API.api_client import api_list, api_get, api_create, api_update, api_delete
from .forms import PlanForm, ActividadForm, ClaseForm, UsuarioForm, BookingForm

API_LOGIN = "http://127.0.0.1:8000/API/api/v1/auth/login/"
API_REFRESH = "http://127.0.0.1:8000/API/api/v1/auth/refresh/"


@login_required
def index(request):
    # KPIs desde API (requiere token)
    planes = api_list(request, "Plan")
    actividades = api_list(request, "Actividad")
    clases = api_list(request, "Clase")

    context = {
        "kpi_planes": len(planes),
        "kpi_actividades": len(actividades),
        "kpi_clases": len(clases),
        "sesiones": clases[:5],
        "actividades": actividades[:8],
    }
    return render(request, "index.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            
            try:
                r = requests.post(
                    API_LOGIN,
                    json={"username": username, "password": password},
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()
                print("Login API json:",data)
                print("Access:",data.get("Access"))
                print("REFRESH:",data.get("refresh"))
                print("Token:",data.get("Token"))
                request.session["api_access"] = data.get("access")
                request.session["api_refresh"] = data.get("refresh")
            except Exception:
                messages.warning(
                    request,
                    "Entraste al sistema, pero no se pudo obtener el token JWT desde la API.",
                )

            next_url = request.GET.get("next") or "index"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    # Borrar tokens de la API + sesión Django
    request.session.pop("api_access", None)
    request.session.pop("api_refresh", None)
    logout(request)
    return redirect("login")


# ------------------ PLANES (API) ------------------
@login_required
def planes_list(request):
    planes = api_list(request, "Plan")
    return render(request, "plans_list.html", {"plans": planes})


@staff_member_required
def cr_plan(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            api_create(request, "Plan", form.cleaned_data)
            return redirect("plans_list")
    else:
        form = PlanForm()
    return render(request, "plans_forms.html", {"form": form, "mode": "create"})


@staff_member_required
def plans_editar(request, plan_id: int):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            api_update(request, "Plan", plan_id, form.cleaned_data)
            return redirect("plans_list")
    else:
        obj = api_get(request, "Plan", plan_id)
        form = PlanForm(initial=obj)
    return render(request, "plans_forms.html", {"form": form, "mode": "edit"})


@staff_member_required
def plans_br(request, plan_id: int):
    if request.method == "POST":
        api_delete(request, "Plan", plan_id)
    return redirect("plans_list")


# ------------------ ACTIVIDADES (API) ------------------
@login_required
def activities_list(request):
    acts = api_list(request, "Actividad")
    return render(request, "activities_list.html", {"activities": acts})


@staff_member_required
def activities_register(request):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            api_create(request, "Actividad", form.cleaned_data)
            return redirect("activities_list")
    else:
        form = ActividadForm()
    return render(request, "activities_forms.html", {"form": form, "mode": "create"})


@staff_member_required
def activities_edit(request, activity_id: int):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            api_update(request, "Actividad", activity_id, form.cleaned_data)
            return redirect("activities_list")
    else:
        obj = api_get(request, "Actividad", activity_id)
        form = ActividadForm(initial=obj)
    return render(request, "activities_forms.html", {"form": form, "mode": "edit"})


@staff_member_required
def activities_delete(request, activity_id: int):
    if request.method == "POST":
        api_delete(request, "Actividad", activity_id)
    return redirect("activities_list")


# ------------------ CLASES (API) ------------------
@login_required
def sessions_list(request):
    clases = api_list(request, "Clase")
    return render(request, "sessions_list.html", {"sessions": clases})


@staff_member_required
def session_estudiante(request, session_id: int):
    clase = api_get(request, "Clase", session_id)
    bookings = api_list(request, "Booking")

    bookings_de_esta_clase = [b for b in bookings if b.get("clase") == session_id]
    usuarios = {u["id"]: u for u in api_list(request, "Usuario")}

    for b in bookings_de_esta_clase:
        u = usuarios.get(b.get("usuario"))
        b["usuario_obj"] = u

    return render(
        request,
        "sessions_estudiante.html",
        {"clase": clase, "bookings": bookings_de_esta_clase},
    )


@login_required
def sessions_register(request):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            api_create(request, "Clase", form.cleaned_data)
            return redirect("sessions_list")
    else:
        form = ClaseForm()
    return render(request, "sessions_form.html", {"form": form, "mode": "create"})


@staff_member_required
def sessions_edit(request, session_id: int):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            api_update(request, "Clase", session_id, form.cleaned_data)
            return redirect("sessions_list")
    else:
        obj = api_get(request, "Clase", session_id)
        form = ClaseForm(initial=obj)
    return render(request, "sessions_form.html", {"form": form, "mode": "edit"})


@staff_member_required
def sessions_delete(request, session_id: int):
    if request.method == "POST":
        api_delete(request, "Clase", session_id)
    return redirect("sessions_list")


# ------------------ USUARIOS (API) ------------------
@staff_member_required
def user_list(request):
    users = api_list(request, "Usuario")
    return render(request, "user_list.html", {"users": users})


@staff_member_required
def user_register(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            api_create(request, "Usuario", form.cleaned_data)
            return redirect("user_list")
    else:
        form = UsuarioForm()
    return render(request, "user_form.html", {"form": form})


# ------------------ BOOKINGS (API) ------------------
@login_required
def bookings_list(request):
    bookings = api_list(request, "Booking")
    return render(request, "bookings_list.html", {"bookings": bookings})


@staff_member_required
def booking_register(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            api_create(request, "Booking", form.cleaned_data)
            return redirect("bookings_list")
    else:
        form = BookingForm()
    return render(request, "bookings_form.html", {"form": form, "mode": "create"})


@staff_member_required
def booking_edit(request, booking_id: int):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            api_update(request, "Booking", booking_id, form.cleaned_data)
            return redirect("bookings_list")
    else:
        obj = api_get(request, "Booking", booking_id)
        form = BookingForm(initial=obj)
    return render(request, "bookings_form.html", {"form": form, "mode": "edit"})


@staff_member_required
def booking_delete(request, booking_id: int):
    if request.method == "POST":
        api_delete(request, "Booking", booking_id)
    return redirect("bookings_list")


@login_required
def panel(request):
    return render(request, "STKAA/panel.html")
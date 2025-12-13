from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .API.api_client import api_list, api_get, api_create, api_update, api_delete
from .forms import PlanForm, ActividadForm, ClaseForm, UsuarioForm, BookingForm


def index(request):
    # KPIs desde API
    planes = api_list("Plan")
    actividades = api_list("Actividad")
    clases = api_list("Clase")

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
            next_url = request.GET.get("next") or "index"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------ PLANES (API) ------------------
def planes_list(request):
    planes = api_list("Plan")
    return render(request, "plans_list.html", {"plans": planes})


@staff_member_required
def cr_plan(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            api_create("Plan", form.cleaned_data)
            return redirect("plans_list")
    else:
        form = PlanForm()
    return render(request, "plans_forms.html", {"form": form, "mode": "create"})


@staff_member_required
def plans_editar(request, plan_id: int):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            api_update("Plan", plan_id, form.cleaned_data)
            return redirect("plans_list")
    else:
        obj = api_get("Plan", plan_id)
        form = PlanForm(initial=obj)
    return render(request, "plans_forms.html", {"form": form, "mode": "edit"})


@staff_member_required
def plans_br(request, plan_id: int):
    if request.method == "POST":
        api_delete("Plan", plan_id)
    return redirect("plans_list")


# ------------------ ACTIVIDADES (API) ------------------
def activities_list(request):
    acts = api_list("Actividad")
    return render(request, "activities_list.html", {"activities": acts})


@staff_member_required
def activities_register(request):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            api_create("Actividad", form.cleaned_data)
            return redirect("activities_list")
    else:
        form = ActividadForm()
    return render(request, "activities_forms.html", {"form": form, "mode": "create"})


@staff_member_required
def activities_edit(request, activity_id: int):
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            api_update("Actividad", activity_id, form.cleaned_data)
            return redirect("activities_list")
    else:
        obj = api_get("Actividad", activity_id)
        form = ActividadForm(initial=obj)
    return render(request, "activities_forms.html", {"form": form, "mode": "edit"})


@staff_member_required
def activities_delete(request, activity_id: int):
    if request.method == "POST":
        api_delete("Actividad", activity_id)
    return redirect("activities_list")


# ------------------ CLASES (API) ------------------
def sessions_list(request):
    clases = api_list("Clase")
    return render(request, "sessions_list.html", {"sessions": clases})

@staff_member_required
def session_estudiante(request, session_id: int):
    clase = api_get("Clase", session_id)
    bookings = api_list("Booking")
    bookings_de_esta_clase = [b for b in bookings if b.get("clase") == session_id]
    usuarios = {u["id"]: u for u in api_list("Usuario")}
    for b in bookings_de_esta_clase:
        u = usuarios.get(b.get("usuario"))
        b["usuario_obj"] = u  # en template: booking.usuario_obj.name

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
            data = form.cleaned_data
            api_create("Clase", data)
            return redirect("sessions_list")
    else:
        form = ClaseForm()
    return render(request, "sessions_form.html", {"form": form, "mode": "create"})


@staff_member_required
def sessions_edit(request, session_id: int):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            api_update("Clase", session_id, form.cleaned_data)
            return redirect("sessions_list")
    else:
        obj = api_get("Clase", session_id)
        form = ClaseForm(initial=obj)
    return render(request, "sessions_form.html", {"form": form, "mode": "edit"})


@staff_member_required
def sessions_delete(request, session_id: int):
    if request.method == "POST":
        api_delete("Clase", session_id)
    return redirect("sessions_list")


# ------------------ USUARIOS (API) ------------------
@staff_member_required
def user_list(request):
    users = api_list("Usuario")
    return render(request, "user_list.html", {"users": users})


@staff_member_required
def user_register(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            api_create("Usuario", form.cleaned_data)
            return redirect("user_list")
    else:
        form = UsuarioForm()
    return render(request, "user_form.html", {"form": form})


# ------------------ BOOKINGS (API) ------------------
@login_required
def bookings_list(request):
    bookings = api_list("Booking")
    return render(request, "bookings_list.html", {"bookings": bookings})


@staff_member_required
def booking_register(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            api_create("Booking", form.cleaned_data)
            return redirect("bookings_list")
    else:
        form = BookingForm()
    return render(request, "bookings_form.html", {"form": form, "mode": "create"})


@staff_member_required
def booking_edit(request, booking_id: int):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            api_update("Booking", booking_id, form.cleaned_data)
            return redirect("bookings_list")
    else:
        obj = api_get("Booking", booking_id)
        form = BookingForm(initial=obj)
    return render(request, "bookings_form.html", {"form": form, "mode": "edit"})


@staff_member_required
def booking_delete(request, booking_id: int):
    if request.method == "POST":
        api_delete("Booking", booking_id)
    return redirect("bookings_list")


@login_required
def panel(request):
    return render(request, 'STKAA/panel.html')
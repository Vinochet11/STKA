from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from STKAA.models import Plan, Actividad, Clase, Usuario, booking as Booking
from STKAA.forms import anadirPlan, ActividadForm, ClaseForm, UsuarioForm, BookingForm


def index(request):
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
        "sesiones": sesiones,
        "actividades": actividades,
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


# ------------------ Funciones de Usuario ------------------
@staff_member_required
def user_list(request):
    users = Usuario.objects.select_related("plan").all().order_by("id")
    return render(request, 'user_list.html', {"users": users})


@staff_member_required
def user_register(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
        print("UsuarioForm errors:", form.errors.as_json())
    else:
        form = UsuarioForm()
    return render(request, "user_form.html", {"form": form})


# ------------------ Funciones de PLANES ------------------
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


# ------------------ Funciones de ACTIVIDADES ------------------
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


# ------------------ FUnciones de CLASES ------------------
def sessions_list(request):
    clases = Clase.objects.select_related("actividad").order_by("inicio")
    return render(request, "sessions_list.html", {"sessions": clases})


@staff_member_required
def session_estudiante(request, session_id):
    clase = get_object_or_404(Clase, pk=session_id)
    bookings = clase.bookings.select_related("usuario").all()

    return render(
        request,
        "sessions_estudiante.html",
        {
            "clase": clase,
            "bookings": bookings,
        },
    )


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


# ------------------ Funciones de BOOKINGS ------------------
@login_required

def bookings_list(request): 
    bookings = ( 
        Booking.objects 
        .select_related("usuario", "clase", "clase__actividad")
        .order_by("clase__inicio") 
          ) 
    return render(request, "bookings_list.html", {"bookings": bookings})



@staff_member_required
def booking_register(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookings_list")
        else:
            print("BookingForm error",form.error.as_json())
    else:
        form = BookingForm()
    return render(request, "bookings_form.html", {"form": form, "mode": "create"})


@staff_member_required
def booking_edit(request, booking_id: int):
    obj = get_object_or_404(Booking, pk=booking_id)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("bookings_list")
    else:
        form = BookingForm(instance=obj)
    return render(request, "bookings_form.html", {"form": form, "mode": "edit"})


@staff_member_required
def booking_delete(request, booking_id: int):
    obj = get_object_or_404(Booking, pk=booking_id)
    if request.method == "POST":
        obj.delete()
    return redirect("bookings_list")



@login_required
def panel(request):
    return render(request, 'STKAA/panel.html')
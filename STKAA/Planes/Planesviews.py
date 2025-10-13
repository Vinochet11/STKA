# STKAA/Planes/Planesviews.py
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from STKAA.Planes.formsPlanes import anadirPlan   # nombre actualizado
from STKAA.models import Plan
from django.shortcuts import render, redirect, get_object_or_404

@staff_member_required
def cr_plan(request):
    if request.method == "POST":
        form = anadirPlan(request.POST)
        if form.is_valid():            
            form.save()
            return redirect("plans_list")
        
        return render(request, "plans_forms.html", {"form": form,"mode":"create"})
    else:
        form = anadirPlan()
    return render(request, "plans_forms.html", {"form": form})

#@login_required
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
    return render(request, 'plans_forms.html', {"form": form, "mode":"edit"})

@staff_member_required
def plans_br(request, plan_id: int):
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == "POST":
        plan.delete()
        return redirect('plans_list')

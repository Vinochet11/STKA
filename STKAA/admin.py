from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    lista_plan=("id","nombre_plan","clases_Mensuales","ilimitado")
    lista_filtro=("ilimitado","nombre_plan")
    busca_PLan=("nombre_plan")
from django.contrib import admin
from .models import Plan,Actividad,Clase

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display=("id","nombre_plan","clases_Mensuales","ilimitado")
    list_filter=("ilimitado","nombre_plan")
    search_fields=("nombre_plan",)
    ordering = ("id",)
    list_per_page= 25

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display=("id","nombre","profesor")
    search_fields=("nombre","profesor")
    ordering= ("id",)
    list_per_page=25

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ("id", "actividad", "inicio", "termino", "estado")
    list_filter = ("estado",)
    search_fields = ("actividad",)
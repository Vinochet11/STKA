##crear una carpeta ej:Planes, por cada uno. dentro de esta for a meter el formulario ej: formPlanes, 
#el template y el views correspondiente.

from django import forms
from STKAA.models import Plan

class anadirPlan(forms.ModelForm):
    class Meta:
        model= Plan
        fields=("nombre_plan","clases_Mensuales","ilimitado")




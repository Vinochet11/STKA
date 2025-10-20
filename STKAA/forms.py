##crear una carpeta ej:Planes, por cada uno. dentro de esta for a meter el formulario ej: formPlanes, 
#el template y el views correspondiente.

from django import forms
from STKAA.models import Plan,Actividad

class anadirPlan(forms.ModelForm):
    class Meta:
        model= Plan
        fields=("nombre_plan","clases_Mensuales","ilimitado")
        widgets={
            "nombre_plan":forms.TextInput(attrs={"class":"form-control"}),
            "clases_mensuales":forms.NumberInput(attrs={"class":"form-control",}),
            "ilimitado":forms.CheckboxInput(attrs={"class":"form-check-input"}), 
        }



class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad 
        fields= ("nombre","profesor")
        widgets={
            "nombre":forms.TextInput(attrs={"class":"form-control","placeholder":"Ej:Boxeo,karate"}),
            "profesor":forms.TextInput(attrs={"class":"form-control",}),
        }       
        error_messages={
             "nombre":{"required":"El nombre de la actividad es obligarotio.","max_length":"Maximo 50 caracteres."},
             "profesor":{"required":"El nombre del profesor es obligatorio ","max_length":"Maximo 50 caracteres"},
            }
##crear una carpeta ej:Planes, por cada uno. dentro de esta for a meter el formulario ej: formPlanes, 
#el template y el views correspondiente.

from django import forms
from STKAA.models import Plan,Actividad, Clase

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
        
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ("actividad", "inicio", "termino", "estado")
        widgets = {
            "actividad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Boxeo"}),
            "inicio": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "termino": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "actividad": {
                "required": "El nombre de la actividad es obligatorio.",
                "max_length": "Máximo 60 caracteres.",
            },
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("inicio")
        termino = cleaned.get("termino")
        if inicio and termino and termino <= inicio:
            self.add_error("termino", "La hora de término debe ser posterior al inicio.")
        return cleaned
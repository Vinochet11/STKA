##crear una carpeta ej:Planes, por cada uno. dentro de esta for a meter el formulario ej: formPlanes, 
#el template y el views correspondiente.

from django import forms
from STKAA.models import Plan,Actividad, Clase,Usuario,booking

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
            "actividad": forms.Select(attrs={"class": "form-select"}),
            "inicio": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "termino": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("inicio")
        termino = cleaned.get("termino")
        if inicio and termino and termino <= inicio:
            self.add_error("termino", "La hora de término debe ser posterior al inicio.")
        return cleaned
    
class UsuarioForm(forms.ModelForm):
    
    plan = forms.ModelChoiceField(
        label="Plan mensual",
        queryset=Plan.objects.none(),      
        required=False,                   
        empty_label="— Selecciona un plan —",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model  = Usuario
        fields = ("name", "email", "password", "rol", "status", "plan")
        widgets = {
            "name":     forms.TextInput(attrs={"class": "form-control"}),
            "email":    forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "rol":      forms.Select(attrs={"class": "form-select"}),
            "status":   forms.Select(attrs={"class": "form-select"}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["plan"].queryset = Plan.objects.order_by("nombre_plan")


class BookingForm(forms.ModelForm):
    class Meta:
        model=booking
        fields=("usuario","clase","estado")
        widgets={
            "usuario":forms.Select(attrs={"class":"form-select"}),
            "clase":forms.Select(attrs={"class":"form-select"}),
            "estado":forms.Select(attrs={"class":"form-select"})
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["usuario"].queryset=Usuario.objects.order_by("name")
        self.fields["clase"].queryset=Clase.objects.select_related("actividad").order_by("inicio")
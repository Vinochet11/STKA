from django import forms
from STKAA.models import Plan,Actividad, Clase,Usuario,booking
from django.core.exceptions import ValidationError

from django import forms

# ---------- PLAN ----------
class PlanForm(forms.Form):
    nombre_plan = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    clases_Mensuales = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    ilimitado = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

# ---------- ACTIVIDAD ----------
class ActividadForm(forms.Form):
    nombre = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Ej: Boxeo, Karate"})
    )
    profesor = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={"class":"form-control"})
    )

# ---------- CLASE ----------
class ClaseForm(forms.Form):
    # OJO: actividad es FK en tu API actual, por eso mandaremos actividad_id (int)
    actividad = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class":"form-control", "placeholder":"ID Actividad"})
    )
    inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type":"datetime-local","class":"form-control"})
    )
    termino = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type":"datetime-local","class":"form-control"})
    )
    estado = forms.ChoiceField(
        choices=[("terminada","terminada"),("cancelada","cancelada"),("programada","programada")],
        widget=forms.Select(attrs={"class":"form-select"})
    )

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("inicio")
        termino = cleaned.get("termino")
        if inicio and termino and termino <= inicio:
            self.add_error("termino", "La hora de término debe ser posterior al inicio.")
        return cleaned

# ---------- USUARIO ----------
class UsuarioForm(forms.Form):
    name = forms.CharField(max_length=45, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    rol = forms.ChoiceField(choices=[("user","user"),("admin","admin")], widget=forms.Select(attrs={"class":"form-select"}))
    status = forms.ChoiceField(choices=[("Activo","Activo"),("Inactivo","Inactivo")], widget=forms.Select(attrs={"class":"form-select"}))
    plan = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"ID Plan (opcional)"}))

# ---------- BOOKING ----------
class BookingForm(forms.Form):
    usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"ID Usuario"}))
    clase = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"ID Clase"}))
    estado = forms.ChoiceField(
        choices=[("asistire","Asistiré"),("cancelada","Cancelada")],
        widget=forms.Select(attrs={"class":"form-select"})
    )

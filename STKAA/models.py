# STKAA/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Plan(models.Model):
    nombre_plan = models.CharField(max_length=50)
    clases_Mensuales = models.PositiveIntegerField(null=True, blank=True)
    ilimitado = models.BooleanField(default=False)

    def clean(self):
        """
        Reglas:
        - nombre_plan obligatorio (no solo espacios).
        - Si ilimitado=True  -> NO se permiten clases_Mensuales (error).
        - Si ilimitado=False -> clases_Mensuales debe ser un entero positivo.
        """
        # nombre obligatorio
        if not (self.nombre_plan or "").strip():
            raise ValidationError({"nombre_plan": "El nombre del plan es obligatorio."})

        
        if self.ilimitado:
            # Si es ilimitado y viene un número, es error
            if self.clases_Mensuales not in (None, 0):
                raise ValidationError({
                    "clases_Mensuales": "No ingrese cantidad de clases si el plan es ilimitado."
                })
            
            self.clases_Mensuales = None
        else:
            # Debe existir y ser > 0
            if self.clases_Mensuales is None or self.clases_Mensuales <= 0:
                raise ValidationError({
                    "clases_Mensuales": "Debe ingresar un número positivo."
                })

    def __str__(self):
        return self.nombre_plan


class Actividad(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        validators=[
            RegexValidator(
                r"^[\wÁÉÍÓÚáéíóúÑñ\s\-]+$",
                "Solo letras/números/espacios/guiones."
            )
        ],
    )
    profesor = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        help_text="Nombre del profesor a cargo de la actividad."
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre
    

class Clase(models.Model):
    
    actividad = models.ForeignKey(Actividad,on_delete=models.PROTECT,related_name="clases",db_column="actividad_id")#el on_delete es para que no se elimine alguna actividad si esque hay clases asociadas
   
    inicio = models.DateTimeField()
    termino = models.DateTimeField()

    ESTADOS = (
        ("terminada", "terminada"),
        ("cancelada", "cancelada"),
        ("programada", "programada"),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="programada")

    def clean(self):
        if self.termino and self.inicio and self.termino <= self.inicio:
            raise ValidationError({"termino": "La hora de término debe ser posterior al inicio."})

    def __str__(self):
        return f"{self.actividad} — {self.inicio:%Y-%m-%d %H:%M}"
    
class Usuario(models.Model):
    ROL_CHOICES    = (("user","user"), ("admin","admin"))
    STATUS_CHOICES = (("Activo","Activo"), ("Inactivo","Inactivo"))

    name     = models.CharField(max_length=45)
    email    = models.EmailField(max_length=100, unique=True,blank=True,null=True)
    password = models.CharField(max_length=128,blank=True,null=True) 
    rol      = models.CharField(max_length=10, choices=ROL_CHOICES, default="user")
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Activo")
    plan     = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL, related_name="usuarios")

    def __str__(self):
        return self.name
    
class booking(models.Model):
    Estados = (
        ("asistire", "Asistiré"),
        ("cancelada", "Cancelada")
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estados,
        default="asistire",
    )
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} -> {self.clase} ({self.estado})"

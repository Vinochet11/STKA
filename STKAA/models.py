
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
        - Si ilimitado=True  -> clases_Mensuales debe quedar vacío (None).
        - Si ilimitado=False -> clases_Mensuales debe ser un entero positivo.
        """
        # nombre obligatorio
        if not (self.nombre_plan or "").strip():
            raise ValidationError({"nombre_plan": "El nombre del plan es obligatorio."})

        if self.ilimitado:
            # Normalizamos a None para no guardar un número que no aplica
            self.clases_Mensuales = None
        else:
            # Debe existir y ser > 0
            if self.clases_Mensuales is None or self.clases_Mensuales <= 0:
                raise ValidationError({"clases_Mensuales": "Debe ingresar un número positivo."})

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
        help_text="Nombre del profesor responsable de la actividad."
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre
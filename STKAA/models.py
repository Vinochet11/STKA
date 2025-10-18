# STKAA/models.py
from django.db import models
from django.core.exceptions import ValidationError

class Plan(models.Model):
    # nombre libre (texto), sin choices => el form será un <input type="text">
    nombre_plan = models.CharField(max_length=50)  # puedes subir el límite si quieres

    # si es ilimitado, este campo puede quedar en blanco
    clases_Mensuales = models.PositiveIntegerField(null=True, blank=True)

    # indica si el plan es ilimitado
    ilimitado = models.BooleanField(default=False)

    def clean(self):
        # Reglas de negocio:
        # - Si es ilimitado → clases_Mensuales debe estar vacío (None o 0)
        # - Si NO es ilimitado → clases_Mensuales debe ser > 0
        if self.ilimitado:
            # normalizamos a None (opcional pero prolijo)
            self.clases_Mensuales = None
        else:
            if self.clases_Mensuales is None or self.clases_Mensuales <= 0:
                raise ValidationError("Para planes con cupo, 'clases_Mensuales' debe ser un número positivo.")

        # Valida que el nombre no esté vacío
        if not (self.nombre_plan or "").strip():
            raise ValidationError("El nombre del plan es obligatorio.")

    def __str__(self):
        return self.nombre_plan
from django.db import models    
from django.core.exceptions import ValidationError

class  Plan(models.Model):
    class Plan_seleccion(models.TextChoices):
        Basico='basico','BASICO'
        AVANZADO='avanzado','Avanzado'
        Premium='premium','PREMIUM'

    nombre_plan=models.CharField(max_length=20,choices=Plan_seleccion.choices)

    clases_Mensuales=models.PositiveIntegerField(null=True, blank=True)
    
    ilimitado=models.BooleanField(default=False)
    
    def __str__(self):
        
        return self.nombre_plan
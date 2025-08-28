from django.db import models
from django_multitenant.models import TenantModelMixin

class Clinic(TenantModelMixin, models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tenant_id = 'id'  # Esto es clave para aislar datos

    def __str__(self):
        return self.name
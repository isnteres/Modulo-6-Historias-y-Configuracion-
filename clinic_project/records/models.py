from django.db import models
from django_multitenant.models import TenantModelMixin
from clinics.models import Clinic

class Record(TenantModelMixin, models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    details = models.TextField()
    tenant_id = 'clinic_id'  # Relación con la clínica

    def __str__(self):
        return f"{self.patient_name} - {self.clinic.name}"
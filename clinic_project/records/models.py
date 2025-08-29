from django.db import models
from django_multitenant.models import TenantModelMixin
from clinics.models import Clinic

class PatientHistory(TenantModelMixin, models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    diagnosis = models.TextField()
    date = models.DateField(auto_now_add=True)

    tenant_id = 'clinic_id'  # se aísla por clínica

    def __str__(self):
        return f"{self.patient_name} ({self.clinic.name})"

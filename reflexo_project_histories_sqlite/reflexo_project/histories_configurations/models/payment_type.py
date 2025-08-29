from django.db import models
from django.utils import timezone
from .tenant import Tenant

class PaymentType(models.Model):
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        related_name="payment_types",
        verbose_name="Clínica"
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'unique': 'Este código ya existe.',
            'max_length': 'El código no debe superar los 50 caracteres.'
        }
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            'unique': 'Este nombre ya existe.',
            'max_length': 'El nombre no debe superar los 255 caracteres.'
        }
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = "payment_types"
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"
        ordering = ["name"]
        unique_together = [['tenant', 'code'], ['tenant', 'name']]  # Único por tenant

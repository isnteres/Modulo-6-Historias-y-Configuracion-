from django.db import models
from django.utils import timezone
from .tenant import Tenant

class DocumentType(models.Model):
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        related_name="document_types",
        verbose_name="Clínica"
    )
    name = models.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )
    description = models.TextField(
        blank=True, null=True,
        error_messages={'max_length': 'La descripción no debe superar los 1000 caracteres.'}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "document_types"
        unique_together = [['tenant', 'name']]  # Nombre único por tenant

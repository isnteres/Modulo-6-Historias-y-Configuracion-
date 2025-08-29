from django.db import models
from django.utils import timezone

class Tenant(models.Model):
    """
    Modelo para representar diferentes clínicas o tenants
    Cada tenant tiene su propio espacio aislado de datos
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Nombre de la Clínica"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Identificador único",
        help_text="Identificador único para la URL (ej: clinica-a, clinica-b)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        """Marca el tenant como eliminado sin borrarlo físicamente"""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        """Restaura un tenant eliminado"""
        self.deleted_at = None
        self.is_active = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tenants"
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"
        ordering = ["name"]

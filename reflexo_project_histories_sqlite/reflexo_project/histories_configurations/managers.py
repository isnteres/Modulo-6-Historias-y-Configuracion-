from django.db import models

class TenantManager(models.Manager):
    """
    Manager personalizado que filtra automáticamente por tenant
    """
    
    def get_queryset(self):
        # Este método será sobrescrito por el middleware
        return super().get_queryset()
    
    def for_tenant(self, tenant):
        """Filtra por tenant específico"""
        return self.get_queryset().filter(tenant=tenant)
    
    def active(self):
        """Filtra solo registros activos (no eliminados)"""
        return self.get_queryset().filter(deleted_at__isnull=True)

class TenantActiveManager(TenantManager):
    """
    Manager que combina filtrado por tenant y solo registros activos
    """
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

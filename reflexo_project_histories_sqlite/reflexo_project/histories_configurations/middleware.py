from django.http import Http404
from django.conf import settings
from .models import Tenant

class TenantMiddleware:
    """
    Middleware para identificar y establecer el tenant actual
    basado en la URL o subdominio
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extraer el tenant de la URL
        # Formato esperado: /tenant-slug/...
        path_parts = request.path.strip('/').split('/')
        
        if path_parts and path_parts[0] not in ['admin', 'static', 'media']:
            tenant_slug = path_parts[0]
            
            try:
                tenant = Tenant.objects.get(
                    slug=tenant_slug, 
                    is_active=True, 
                    deleted_at__isnull=True
                )
                request.tenant = tenant
                
                # Modificar la URL para quitar el tenant
                request.path_info = '/' + '/'.join(path_parts[1:])
                request.path = request.path_info
                
            except Tenant.DoesNotExist:
                # Si no existe el tenant, devolver 404
                raise Http404(f"Clínica '{tenant_slug}' no encontrada")
        else:
            # Para rutas sin tenant (admin, static, etc.)
            request.tenant = None

        response = self.get_response(request)
        return response

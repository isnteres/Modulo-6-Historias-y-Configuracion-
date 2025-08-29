from clinics.models import Clinic
from django_multitenant.utils import set_current_tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Identificar la clínica actual
        clinic_id = request.headers.get('X-CLINIC-ID') or request.GET.get('clinic_id')

        if clinic_id:
            try:
                clinic = Clinic.objects.get(id=clinic_id)
                set_current_tenant(clinic)
            except Clinic.DoesNotExist:
                pass  # Si no existe, no asignamos tenant

        return self.get_response(request)
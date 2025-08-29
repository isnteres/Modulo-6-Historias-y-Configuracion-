from django.core.management.base import BaseCommand
from histories_configurations.models import Tenant, DocumentType, PaymentType, PredeterminedPrice

class Command(BaseCommand):
    help = 'Crea datos iniciales básicos para cada tenant del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos iniciales por tenant...')
        
        # Obtener todos los tenants activos
        tenants = Tenant.objects.filter(is_active=True, deleted_at__isnull=True)
        
        if not tenants.exists():
            self.stdout.write(self.style.ERROR('No hay tenants activos. Ejecuta primero: python manage.py create_tenants'))
            return
        
        for tenant in tenants:
            self.stdout.write(f'\n--- Creando datos para {tenant.name} ---')
            
            # Crear tipos de documento básicos
            document_types = [
                {'name': 'DNI', 'description': 'Documento Nacional de Identidad'},
                {'name': 'CE', 'description': 'Carnet de Extranjería'},
                {'name': 'Pasaporte', 'description': 'Pasaporte'},
                {'name': 'RUC', 'description': 'Registro Único de Contribuyentes'},
            ]
            
            for dt_data in document_types:
                dt, created = DocumentType.objects.get_or_create(
                    tenant=tenant,
                    name=dt_data['name'],
                    defaults={'description': dt_data['description']}
                )
                if created:
                    self.stdout.write(f'✓ Creado tipo de documento: {dt.name}')
                else:
                    self.stdout.write(f'• Tipo de documento ya existe: {dt.name}')
            
            # Crear tipos de pago básicos
            payment_types = [
                {'code': 'EFE', 'name': 'Efectivo'},
                {'code': 'YAP', 'name': 'Yape'},
                {'code': 'PLI', 'name': 'Plin'},
                {'code': 'TRA', 'name': 'Transferencia'},
                {'code': 'TAR', 'name': 'Tarjeta'},
            ]
            
            for pt_data in payment_types:
                pt, created = PaymentType.objects.get_or_create(
                    tenant=tenant,
                    name=pt_data['name'],
                    defaults={'code': pt_data['code']}
                )
                if created:
                    self.stdout.write(f'✓ Creado tipo de pago: {pt.name}')
                else:
                    self.stdout.write(f'• Tipo de pago ya existe: {pt.name}')
            
            # Crear precios predeterminados básicos
            predetermined_prices = [
                {'name': 'Consulta Estándar', 'price': 50.00},
                {'name': 'Consulta Premium', 'price': 80.00},
                {'name': 'Terapia Completa', 'price': 120.00},
            ]
            
            for pp_data in predetermined_prices:
                pp, created = PredeterminedPrice.objects.get_or_create(
                    tenant=tenant,
                    name=pp_data['name'],
                    defaults={'price': pp_data['price']}
                )
                if created:
                    self.stdout.write(f'✓ Creado precio predeterminado: {pp.name}')
                else:
                    self.stdout.write(f'• Precio predeterminado ya existe: {pp.name}')
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos iniciales creados exitosamente para todos los tenants!'))

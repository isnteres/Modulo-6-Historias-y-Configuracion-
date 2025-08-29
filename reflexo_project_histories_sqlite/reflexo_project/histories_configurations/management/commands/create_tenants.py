from django.core.management.base import BaseCommand
from histories_configurations.models import Tenant

class Command(BaseCommand):
    help = 'Crea los tenants iniciales (clínicas) del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Creando tenants iniciales...')
        
        # Crear Clínica A
        clinica_a, created = Tenant.objects.get_or_create(
            slug='clinica-a',
            defaults={
                'name': 'Clínica A',
                'description': 'Clínica principal de reflexología y terapias alternativas',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'✓ Creada Clínica A: {clinica_a.name}')
        else:
            self.stdout.write(f'• Clínica A ya existe: {clinica_a.name}')
        
        # Crear Clínica B
        clinica_b, created = Tenant.objects.get_or_create(
            slug='clinica-b',
            defaults={
                'name': 'Clínica B',
                'description': 'Sucursal especializada en tratamientos avanzados',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'✓ Creada Clínica B: {clinica_b.name}')
        else:
            self.stdout.write(f'• Clínica B ya existe: {clinica_b.name}')
        
        self.stdout.write(self.style.SUCCESS('¡Tenants creados exitosamente!'))
        self.stdout.write('URLs disponibles:')
        self.stdout.write(f'  - Clínica A: /clinica-a/')
        self.stdout.write(f'  - Clínica B: /clinica-b/')

from django.contrib import admin
from .models import Clinic  # <-- Nombre correcto

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "address")  # Columnas que quieres mostrar en el admin

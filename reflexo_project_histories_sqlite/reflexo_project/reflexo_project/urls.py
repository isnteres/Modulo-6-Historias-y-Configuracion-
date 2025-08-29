from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs con tenant: /clinica-a/histories_configurations/...
    path('<str:tenant_slug>/', include('histories_configurations.urls')),
    # URL raíz para selección de clínica
    path('', lambda r: render(r, 'tenant_selection.html')),
]

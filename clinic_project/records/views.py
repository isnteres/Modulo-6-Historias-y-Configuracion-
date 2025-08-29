from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PatientHistory

@login_required
def list_histories(request):
    # Obtiene todas las clínicas del usuario
    clinics = request.user.clinics.all()
    histories = PatientHistory.objects.filter(clinic__in=clinics)
    return render(request, "histories.html", {"histories": histories})

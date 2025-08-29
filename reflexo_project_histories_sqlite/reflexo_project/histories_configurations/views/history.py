import json
import logging
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ..models import History, DocumentType

logger = logging.getLogger(__name__)

@csrf_exempt
def histories_list(request):
    try:
        if request.method != "GET":
            return HttpResponseNotAllowed(["GET"])
        
        # Filtrar por tenant actual
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return JsonResponse({"error": "Clínica no especificada"}, status=400)
        
        qs = History.objects.filter(
            tenant=tenant,
            deleted_at__isnull=True
        ).select_related("document_type")
        
        data = [{
            "id": h.id,
            "document_type": h.document_type.name,
            "document_number": h.document_number,
            "full_name": getattr(h, 'full_name', ''),
            "height": h.height,
            "weight": h.weight,
            "payment_type": getattr(h, 'payment_type', ''),
            "amount": h.amount,
            "observation": getattr(h, 'observation', ''),
            "created_at": h.created_at.isoformat() if h.created_at else None
        } for h in qs]
        return JsonResponse({"histories": data})
    except Exception as e:
        logger.error(f"Error en histories_list: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)


@csrf_exempt
def history_create(request):
    try:
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        
        # Verificar tenant
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return JsonResponse({"error": "Clínica no especificada"}, status=400)
        
        # Manejo de JSON inválido
        try:
            payload = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        
        document_type_name = payload.get("document_type")
        document_number = payload.get("document_number")

        # Validar campos obligatorios
        if not document_type_name or not document_number:
            return JsonResponse({"error": "Campos obligatorios faltantes"}, status=400)

        
        try:
            dt = DocumentType.objects.get(
                tenant=tenant,
                name=document_type_name, 
                deleted_at__isnull=True
            )
        except DocumentType.DoesNotExist:
            return JsonResponse({"error": f"Tipo de documento '{document_type_name}' no encontrado en esta clínica"}, status=400)
        
        # Verificar si ya existe un historial activo con esta combinación en este tenant
        existing_history = History.objects.filter(
            tenant=tenant,
            document_type=dt,
            document_number=document_number,
            deleted_at__isnull=True
        ).first()
        
        if existing_history:
            return JsonResponse({
                "error": "Ya existe un historial activo con este tipo de documento y número en esta clínica",
                "existing_history_id": existing_history.id
            }, status=409)
        
        try:
            h = History.objects.create(
                tenant=tenant,
                document_type=dt, 
                document_number=document_number
            )
            return JsonResponse({"id": h.id}, status=201)
        except Exception as e:
            logger.error(f"Error al crear historial: {str(e)}")
            return JsonResponse({"error": "Error al crear el historial"}, status=500)
            
    except Exception as e:
        logger.error(f"Error inesperado en history_create: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

@csrf_exempt
def history_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    
    h.soft_delete()  # Debe marcar deleted_at = timezone.now()
    return JsonResponse({"status": "deleted"})

@csrf_exempt
def history_update(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"Historial no encontrado"}, status=404)
    
    # Actualizar campos permitidos
    allowed_fields = ['full_name', 'height', 'weight', 'payment_type', 'amount', 'observation']
    for field in allowed_fields:
        if field in payload:
            setattr(h, field, payload[field])
    
    h.save()
    
    return JsonResponse({
        "id": h.id,
        "document_type": h.document_type.name,  # Cambiado de h.document_type_id a h.document_type.name
        "document_number": h.document_number,
        "full_name": getattr(h, 'full_name', ''),
        "height": h.height,
        "weight": h.weight,
        "payment_type": getattr(h, 'payment_type', ''),
        "amount": getattr(h, 'amount', None),
        "observation": getattr(h, 'observation', '')
    })

@csrf_exempt
def history_entry_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    history_id = payload.get("history_id")
    if not history_id:
        return JsonResponse({"error": "history_id es requerido"}, status=400)
    
    try:
        history = History.objects.filter(deleted_at__isnull=True).get(pk=history_id)
    except History.DoesNotExist:
        return JsonResponse({"error": "Historial no encontrado"}, status=404)
    
    # Crear la entrada del historial
    from ..models import HistoryEntry
    entry = HistoryEntry.objects.create(
        history=history,
        date=payload.get("date"),
        therapist=payload.get("therapist"),
        diagnosis=payload.get("diagnosis"),
        ailments=payload.get("ailments"),
        medications=payload.get("medications"),
        observations=payload.get("observations"),
        height=payload.get("height"),
        weight=payload.get("weight"),
        testimony=payload.get("testimony", "No"),
        payment_type=payload.get("payment_type"),
        reflex=payload.get("reflex")
    )
    
    return JsonResponse({
        "id": entry.id,
        "date": entry.date.isoformat(),
        "therapist": entry.therapist,
        "diagnosis": entry.diagnosis,
        "ailments": entry.ailments,
        "medications": entry.medications,
        "observations": entry.observations,
        "height": entry.height,
        "weight": entry.weight,
        "testimony": entry.testimony,
        "payment_type": entry.payment_type,
        "reflex": entry.reflex,
        "created_at": entry.created_at.isoformat()
    }, status=201)
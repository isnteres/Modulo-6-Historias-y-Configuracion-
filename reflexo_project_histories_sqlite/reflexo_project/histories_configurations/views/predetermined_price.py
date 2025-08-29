import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models import PredeterminedPrice

@csrf_exempt
def predetermined_prices_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = PredeterminedPrice.objects.filter(deleted_at__isnull=True)
    data = [{
        "id": x.id, 
        "name": x.name, 
        "price": float(x.price) if x.price else None
    } for x in qs]
    return JsonResponse({"predetermined_prices": data})

@csrf_exempt
def predetermined_price_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    name = payload.get("name", "").strip()
    price = payload.get("price")
    
    if not name:
        return JsonResponse({"error": "El nombre es requerido"}, status=400)
    
    if price is not None:
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({"error": "El precio debe ser mayor a 0"}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "El precio debe ser un número válido"}, status=400)
    
    # Verificar si ya existe un precio predeterminado con este nombre
    existing_price = PredeterminedPrice.objects.filter(
        name__iexact=name,
        deleted_at__isnull=True
    ).first()
    
    if existing_price:
        return JsonResponse({
            "error": "Ya existe un precio predeterminado con este nombre"
        }, status=409)
    
    try:
        pp = PredeterminedPrice.objects.create(name=name, price=price)
        return JsonResponse({
            "id": pp.id, 
            "name": pp.name, 
            "price": float(pp.price) if pp.price else None
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": "Error al crear el precio predeterminado"}, status=500)

@csrf_exempt
def predetermined_price_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        pp = PredeterminedPrice.objects.get(pk=pk, deleted_at__isnull=True)
    except PredeterminedPrice.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    pp.soft_delete()
    return JsonResponse({"status": "deleted", "id": pk})

@csrf_exempt
def predetermined_price_edit(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    try:
        pp = PredeterminedPrice.objects.get(pk=pk, deleted_at__isnull=True)
    except PredeterminedPrice.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    name = payload.get("name", "").strip()
    price = payload.get("price")
    
    if not name:
        return JsonResponse({"error": "El nombre es requerido"}, status=400)
    
    if price is not None:
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({"error": "El precio debe ser mayor a 0"}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "El precio debe ser un número válido"}, status=400)
    
    # Verificar si ya existe otro precio predeterminado con este nombre
    existing_price = PredeterminedPrice.objects.filter(
        name__iexact=name,
        deleted_at__isnull=True
    ).exclude(pk=pk).first()
    
    if existing_price:
        return JsonResponse({
            "error": "Ya existe un precio predeterminado con este nombre"
        }, status=409)
    
    pp.name = name
    pp.price = price
    pp.save()
    
    return JsonResponse({
        "id": pp.id, 
        "name": pp.name, 
        "price": float(pp.price) if pp.price else None
    })

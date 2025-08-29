from django.urls import path
from .views import history, document_types_list, document_type_create, document_type_delete
from .views import payment_types_list, payment_type_create, payment_type_delete, payment_type_edit # Importa las vistas de PaymentType
from .views import predetermined_price

urlpatterns = [
    # Solo las rutas que existen
    path("histories/", history.histories_list, name="histories_list"),
    path("histories/create/", history.history_create, name="history_create"),
    path("histories/<int:pk>/delete/", history.history_delete, name="history_delete"),
    path("histories/<int:pk>/update/", history.history_update, name="history_update"),
    path("histories/entries/create/", history.history_entry_create, name="history_entry_create"),

    path("document_types/", document_types_list, name="document_types_list"),  # Para listar tipos de documento
    path("document_types/create/", document_type_create, name="document_type_create"),  # Para crear un tipo de documento
    path("document_types/<int:pk>/delete/", document_type_delete, name="document_type_delete"),  # Para eliminar un tipo de documento

    path("payment_types/", payment_types_list, name="payment_types_list"),  # Para listar tipos de pago
    path("payment_types/create/", payment_type_create, name="payment_type_create"),  # Para crear un tipo de pago
    path("payment_types/<int:pk>/delete/", payment_type_delete, name="payment_type_delete"),  # Para eliminar un tipo de pago
    path('payment_types/<int:pk>/edit/', payment_type_edit, name='payment_type_edit'),

    # Pagos Predeterminados
    path("predetermined_prices/", predetermined_price.predetermined_prices_list, name="predetermined_prices_list"),
    path("predetermined_prices/create/", predetermined_price.predetermined_price_create, name="predetermined_price_create"),
    path("predetermined_prices/<int:pk>/delete/", predetermined_price.predetermined_price_delete, name="predetermined_price_delete"),
    path("predetermined_prices/<int:pk>/edit/", predetermined_price.predetermined_price_edit, name="predetermined_price_edit"),

    #TODO: Agregar más endpoints cuando estén implementados
]

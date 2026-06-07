from django.urls import path
from .views import processar_pagamento

urlpatterns = [
    path("processar/", processar_pagamento),
]
from django.urls import path
from .views import criar_agendamento

urlpatterns = [
    path('agendar/', criar_agendamento),
]
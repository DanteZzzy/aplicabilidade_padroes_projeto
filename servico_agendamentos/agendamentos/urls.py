from django.urls import path
from .views import criar_agendamento

urlpatterns = [
    path('', criar_agendamento),
]
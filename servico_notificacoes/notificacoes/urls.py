from django.urls import path
from .views import notificar

urlpatterns = [
    path("notificar/", notificar),
]
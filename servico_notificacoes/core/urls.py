from django.urls import path, include

urlpatterns = [
    path("notificacoes/", include("notificacoes.urls")),
]
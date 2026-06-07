from django.urls import path, include

urlpatterns = [
    path("pagamentos/", include("pagamentos.urls")),
]
from django.contrib import admin
from .models import Agendamento, Servico

admin.site.register(Agendamento)
admin.site.register(Servico)
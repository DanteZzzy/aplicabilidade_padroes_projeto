from django.db import models
from django.utils import timezone

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    tipo = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class Agendamento(models.Model):
    cliente = models.CharField(max_length=100)
    data_hora = models.DateTimeField(default=timezone.now)
    pagamento = models.CharField(max_length=20)
    valor_total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    pago = models.BooleanField(default=False)
    servicos = models.ManyToManyField(Servico) 
    data_criacao = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.cliente} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
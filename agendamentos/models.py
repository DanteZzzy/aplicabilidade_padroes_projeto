from django.db import models


class Servico(models.Model):

    nome = models.CharField(max_length=100)

    tipo = models.CharField(max_length=50)

    preco = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    def __str__(self):
        return self.nome


class Agendamento(models.Model):

    PAGAMENTO_CHOICES = [
        ('pix', 'Pix'),
        ('cartao', 'Cartão'),
    ]

    cliente = models.CharField(max_length=100)

    servicos = models.ManyToManyField(Servico)

    valor_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    data = models.DateTimeField(auto_now_add=True)

    pagamento = models.CharField(
        max_length=20,
        choices=PAGAMENTO_CHOICES,
        default='pix'
    )

    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.cliente
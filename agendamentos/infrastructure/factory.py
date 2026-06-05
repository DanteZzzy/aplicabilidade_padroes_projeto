from agendamentos.models import Servico

class ServiceFactory:
    @staticmethod
    def criar_servicos_padrao():
        if not Servico.objects.exists():
            Servico.objects.create(nome="Corte Social", preco=20.00, tipo="corte")
            Servico.objects.create(nome="Corte Degradê", preco=25.00, tipo="corte")
            Servico.objects.create(nome="Barba Alinhada", preco=15.00, tipo="barba")
            Servico.objects.create(nome="Barba com toalha quente", preco=20.00, tipo="barba")
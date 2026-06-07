from abc import ABC, abstractmethod
from agendamentos.models import Servico


class ServicoFactory(ABC):

    @abstractmethod
    def criar(self, nome, preco):
        pass


class CorteFactory(ServicoFactory):

    def criar(self, nome, preco):
        return Servico.objects.get_or_create(
            nome=nome,
            defaults={"tipo": "corte", "preco": preco}
        )[0]


class BarbaFactory(ServicoFactory):

    def criar(self, nome, preco):
        return Servico.objects.get_or_create(
            nome=nome,
            defaults={"tipo": "barba", "preco": preco}
        )[0]


class ServiceFactory:

    FACTORIES = {
        "corte": CorteFactory,
        "barba": BarbaFactory,
    }

    @staticmethod
    def criar_servicos_padrao():
        ServiceFactory.criar("corte", "Corte Social", 20.00)
        ServiceFactory.criar("corte", "Corte Degradê", 25.00)
        ServiceFactory.criar("barba", "Barba Alinhada", 15.00)
        ServiceFactory.criar("barba", "Barba com toalha quente", 20.00)

    @staticmethod
    def criar(tipo, nome, preco):
        factory_class = ServiceFactory.FACTORIES.get(tipo)

        if not factory_class:
            raise ValueError(f"Tipo de serviço inválido: {tipo}")

        return factory_class().criar(nome, preco)
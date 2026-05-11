from agendamentos.models import Servico


class ServiceFactory:

    @staticmethod
    def criar(tipo, nome, preco):
        return Servico.objects.get_or_create(
            nome=nome,
            defaults={"tipo": tipo, "preco": preco}
        )[0]

    @staticmethod
    def criar_corte(nome, preco):
        return ServiceFactory.criar("corte", nome, preco)

    @staticmethod
    def criar_barba(nome, preco):
        return ServiceFactory.criar("barba", nome, preco)

    @staticmethod
    def criar_servicos_padrao():
        ServiceFactory.criar_corte("Corte Social", 25)
        ServiceFactory.criar_corte("Corte Degradê", 30)
        ServiceFactory.criar_barba("Barba", 20)
        ServiceFactory.criar_barba("Barba (com toalha quente)", 25)
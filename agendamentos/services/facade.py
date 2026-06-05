from agendamentos.models import Agendamento
from .strategy import PaymentStrategy, PixPayment, CartaoPayment
from .observer import Subject, AgendamentoSubject, EmailNotifier, LogNotifier


PAYMENT_STRATEGIES = {
    "pix": PixPayment,
    "cartao": CartaoPayment,
}


class AgendamentoFacade:

    def __init__(self, subject: Subject = None):
        self.subject = subject or AgendamentoSubject()
        self.subject.add_observer(EmailNotifier())
        self.subject.add_observer(LogNotifier())

    def _get_payment_strategy(self, metodo_pagamento) -> PaymentStrategy:
        strategy_class = PAYMENT_STRATEGIES.get(metodo_pagamento)

        if not strategy_class:
            return None

        return strategy_class()

    def criar_agendamento(self, cliente, servicos, metodo_pagamento):

        # SOMA DOS SERVIÇOS
        valor_total = sum(servico.preco for servico in servicos)

        # STRATEGY — via abstração, sem if/elif
        pagamento_strategy = self._get_payment_strategy(metodo_pagamento)

        if not pagamento_strategy:
            return {
                "status": "erro",
                "mensagem": "Forma de pagamento inválida."
            }

        # EXECUTA PAGAMENTO
        resultado_pagamento = pagamento_strategy.pagar(valor_total)

        if resultado_pagamento["status"] != "sucesso":
            return {
                "status": "erro",
                "mensagem": "Não foi possível concluir o pagamento."
            }

        # CRIA AGENDAMENTO
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            pagamento=metodo_pagamento,
            valor_total=resultado_pagamento["valor_final"],
            pago=True
        )

        # MANY TO MANY
        agendamento.servicos.set(servicos)

        # OBSERVER
        self.subject.notify(agendamento)

        return {
            "status": "sucesso",
            "agendamento": agendamento,
            "mensagem": f"Agendamento concluído para {cliente}",
            "pagamento_msg": resultado_pagamento["mensagem"]
        }
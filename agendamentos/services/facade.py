from agendamentos.models import Agendamento
from .strategy import PixPayment, CartaoPayment
from .observer import AgendamentoSubject, EmailNotifier, LogNotifier


class AgendamentoFacade:

    def criar_agendamento(self, cliente, servicos, metodo_pagamento):

        # SOMA DOS SERVIÇOS
        valor_total = sum(servico.preco for servico in servicos)

        # STRATEGY
        if metodo_pagamento == "pix":

            pagamento_strategy = PixPayment()

        elif metodo_pagamento == "cartao":

            pagamento_strategy = CartaoPayment()

        else:
            return {
                "status": "erro",
                "mensagem": "Forma de pagamento inválida."
            }

        # EXECUTA PAGAMENTO
        resultado_pagamento = pagamento_strategy.pagar(valor_total)

        # SE DER ERRO
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
        subject = AgendamentoSubject()

        subject.add_observer(EmailNotifier())
        subject.add_observer(LogNotifier())

        subject.notify(agendamento)

        return {
            "status": "sucesso",
            "agendamento": agendamento,
            "mensagem": f"Agendamento concluído para {cliente}",
            "pagamento_msg": resultado_pagamento["mensagem"]
        }
from decimal import Decimal
from django.utils import timezone
import requests


class CriarAgendamentoUseCase:

    PAGAMENTO_URL = "http://pagamentos:8001/pagamentos/processar/"
    NOTIFICACAO_URL = "http://notificacoes:8002/notificacoes/notificar/"

    def __init__(self, repository):
        self.repository = repository

    def executar(self, cliente: str, data_agendada, metodo_pagamento: str, servicos: list):

        if data_agendada < timezone.now():
            return {
                "status": "erro",
                "mensagem": "Não é possível agendar para uma data que já passou."
            }

        if self.repository.verificar_horario_existente(data_agendada):
            return {
                "status": "erro",
                "mensagem": "Este horário já está reservado. Escolha outro momento."
            }

        if not servicos:
            return {"status": "erro", "mensagem": "Selecione ao menos um serviço."}

        valor_total = sum(Decimal(str(s.preco)) for s in servicos)

        # CHAMA MICROSSERVIÇO DE PAGAMENTO
        try:
            resposta_pagamento = requests.post(self.PAGAMENTO_URL, json={
                "metodo_pagamento": metodo_pagamento,
                "valor": str(valor_total)
            })
            resultado_pagamento = resposta_pagamento.json()
        except Exception:
            return {"status": "erro", "mensagem": "Serviço de pagamento indisponível."}

        if resultado_pagamento["status"] != "sucesso":
            return {"status": "erro", "mensagem": resultado_pagamento["mensagem"]}

        agendamento = self.repository.salvar_agendamento(
            cliente=cliente,
            data_hora=data_agendada,
            metodo_pagamento=metodo_pagamento,
            valor_total=Decimal(resultado_pagamento["valor_final"]),
            servicos=servicos
        )

        # CHAMA MICROSSERVIÇO DE NOTIFICAÇÃO
        try:
            requests.post(self.NOTIFICACAO_URL, json={
                "cliente": cliente,
                "data_hora": str(data_agendada)
            })
        except Exception:
            pass  # Notificação não bloqueia o fluxo

        return {
            "status": "sucesso",
            "agendamento": agendamento,
            "mensagem": f"Agendamento concluído para {cliente}!",
            "pagamento_msg": resultado_pagamento["mensagem"]
        }
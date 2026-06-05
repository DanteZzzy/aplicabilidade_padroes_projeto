from decimal import Decimal
from django.utils import timezone
from .strategy import PaymentStrategy, PixPayment, CartaoPayment
from .observer import Subject, AgendamentoSubject, EmailNotifier, LogNotifier

PAYMENT_STRATEGIES = {
    "pix": PixPayment,
    "cartao": CartaoPayment,
}

class CriarAgendamentoUseCase:

    def __init__(self, repository, subject: Subject = None):
        self.repository = repository
        self.subject = subject or AgendamentoSubject()
        self.subject.add_observer(EmailNotifier())
        self.subject.add_observer(LogNotifier())

    def _get_payment_strategy(self, metodo_pagamento) -> PaymentStrategy:
        strategy_class = PAYMENT_STRATEGIES.get(metodo_pagamento)
        return strategy_class() if strategy_class else None

    def executar(self, cliente: str, data_agendada, metodo_pagamento: str, servicos: list):
        # 1. Validação de data no passado
        if data_agendada < timezone.now():
            return {
                "status": "erro",
                "mensagem": "Não é possível realizar um agendamento para uma data ou horário que já passou."
            }

        # 2. Validação de horário duplicado (Sua Regra: se já estiver lá, ignora)
        if self.repository.verificar_horario_existente(data_agendada):
            return {
                "status": "erro",
                "mensagem": "Este horário já está reservado por outro cliente. Escolha outro momento."
            }

        if not servicos:
            return {"status": "erro", "mensagem": "Selecione ao menos um serviço para agendar."}

        # 3. Soma dinâmica do valor dos serviços selecionados
        valor_total_servicos = sum(Decimal(str(servico.preco)) for servico in servicos)

        # 4. Executa a estratégia de pagamento
        pagamento_strategy = self._get_payment_strategy(metodo_pagamento)
        if not pagamento_strategy:
            return {"status": "erro", "mensagem": "Forma de pagamento inválida."}

        resultado_pagamento = pagamento_strategy.pagar(valor_total_servicos)
        if resultado_pagamento["status"] != "sucesso":
            return {"status": "erro", "mensagem": "Não foi possível processar o pagamento."}

        # 5. Salva no repositório passando a lista de serviços
        agendamento = self.repository.salvar_agendamento(
            cliente=cliente,
            data_hora=data_agendada,
            metodo_pagamento=metodo_pagamento,
            valor_total=resultado_pagamento["valor_final"],
            servicos=servicos
        )

        # 6. Notifica os observadores (Observer Pattern)
        self.subject.notify(agendamento)

        return {
            "status": "sucesso",
            "agendamento": agendamento,
            "mensagem": f"Agendamento concluído com sucesso para {cliente}!",
            "pagamento_msg": resultado_pagamento["mensagem"]
        }
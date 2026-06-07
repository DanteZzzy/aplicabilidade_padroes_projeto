from agendamentos.models import Agendamento
from agendamentos.domain.repositories import AgendamentoRepositoryInterface


class DjangoAgendamentoRepository(AgendamentoRepositoryInterface):

    def salvar_agendamento(self, cliente: str, data_hora, metodo_pagamento: str, valor_total: float, servicos: list):
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            data_hora=data_hora,
            pagamento=metodo_pagamento,
            valor_total=valor_total,
            pago=True
        )
        agendamento.servicos.set(servicos)
        return agendamento

    def verificar_horario_existente(self, data_hora) -> bool:
        return Agendamento.objects.filter(data_hora=data_hora).exists()
from behave import given, when, then
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch


@given('que o cliente "{nome}" quer agendar para daqui 24 horas')
def step_cliente_data_futura(context, nome):
    context.cliente = nome
    context.data_agendada = timezone.now() + timedelta(hours=24)
    context.horario_duplicado = False


@given('que o cliente "{nome}" quer agendar para 1 hora atrás')
def step_cliente_data_passada(context, nome):
    context.cliente = nome
    context.data_agendada = timezone.now() - timedelta(hours=1)
    context.horario_duplicado = False


@given('escolheu o serviço "{nome}" por R$ {preco}')
def step_servico(context, nome, preco):
    servico = MagicMock()
    servico.nome = nome
    servico.preco = Decimal(preco)
    context.servicos = [servico]


@given('não selecionou nenhum serviço')
def step_sem_servico(context):
    context.servicos = []


@given('selecionou pagamento via "{metodo}"')
def step_pagamento(context, metodo):
    context.metodo_pagamento = metodo


@given('o horário já está reservado')
def step_horario_reservado(context):
    context.horario_duplicado = True


@when('o agendamento for confirmado')
def step_confirmar(context):
    from agendamentos.use_cases.criar_agendamento import CriarAgendamentoUseCase

    repository = MagicMock()
    repository.verificar_horario_existente.return_value = context.horario_duplicado
    repository.salvar_agendamento.return_value = MagicMock(cliente=context.cliente)

    use_case = CriarAgendamentoUseCase(repository=repository)

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "status": "sucesso",
            "valor_final": "20.00",
            "mensagem": "Pagamento via PIX confirmado. Total: R$ 20.00"
        }
        context.resultado = use_case.executar(
            cliente=context.cliente,
            data_agendada=context.data_agendada,
            metodo_pagamento=context.metodo_pagamento,
            servicos=context.servicos
        )


@then('o resultado deve ser "{status}"')
def step_verificar_status(context, status):
    assert context.resultado["status"] == status, \
        f"Esperado '{status}', recebido '{context.resultado['status']}'"


@then('a mensagem deve conter "{trecho}"')
def step_verificar_mensagem(context, trecho):
    assert trecho in context.resultado["mensagem"], \
        f"'{trecho}' não encontrado em '{context.resultado['mensagem']}'"
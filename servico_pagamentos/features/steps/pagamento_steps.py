from behave import given, when, then
from decimal import Decimal
from pagamentos.strategy import PixPayment, CartaoPayment

STRATEGIES = {
    "pix": PixPayment,
    "cartao": CartaoPayment,
}

@given('que o valor do serviço é R$ {valor}')
def step_valor(context, valor):
    context.valor = Decimal(valor)

@given('o método de pagamento é "{metodo}"')
def step_metodo(context, metodo):
    context.metodo = metodo

@when('o pagamento for processado')
def step_processar(context):
    strategy_class = STRATEGIES.get(context.metodo)
    if not strategy_class:
        context.resultado = {"status": "erro", "mensagem": "Forma de pagamento inválida."}
    else:
        context.resultado = strategy_class().pagar(context.valor)

@then('o status do pagamento deve ser "{status}"')
def step_verificar_status(context, status):
    assert context.resultado["status"] == status, \
        f"Esperado '{status}', recebido '{context.resultado['status']}'"
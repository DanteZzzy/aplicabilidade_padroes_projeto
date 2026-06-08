from behave import given, when, then
from notificacoes.observer import AgendamentoSubject, EmailNotifier, LogNotifier


@given('que um agendamento foi criado para "{cliente}"')
def step_cliente(context, cliente):
    context.cliente = cliente
    context.notificados = []
    context.num_observers = 1

@given('a data do agendamento é "{data_hora}"')
def step_data(context, data_hora):
    context.data_hora = data_hora

@given('existem {num} observers registrados')
def step_observers(context, num):
    context.num_observers = int(num)

@when('a notificação for disparada')
def step_notificar(context):
    class TestNotifier(EmailNotifier):
        def __init__(self, lista):
            self.lista = lista
        def update(self, agendamento):
            self.lista.append(agendamento["cliente"])

    subject = AgendamentoSubject()
    for _ in range(context.num_observers):
        subject.add_observer(TestNotifier(context.notificados))

    subject.notify({"cliente": context.cliente, "data_hora": context.data_hora})

@then('todos os observers devem ser notificados')
def step_verificar(context):
    assert len(context.notificados) == context.num_observers, \
        f"Esperado {context.num_observers} notificações, recebido {len(context.notificados)}"
    assert all(n == context.cliente for n in context.notificados)
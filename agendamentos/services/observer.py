class Observer:
    def update(self, agendamento):
        pass


class EmailNotifier(Observer):
    def update(self, agendamento):
        print(f"[EMAIL] Enviado para {agendamento.cliente}")


class LogNotifier(Observer):
    def update(self, agendamento):
        print(f"[LOG] Novo agendamento criado -> {agendamento}")


class AgendamentoSubject:
    def __init__(self):
        self.observers = []

    def add_observer(self, obs):
        self.observers.append(obs)

    def notify(self, agendamento):
        for obs in self.observers:
            obs.update(agendamento)
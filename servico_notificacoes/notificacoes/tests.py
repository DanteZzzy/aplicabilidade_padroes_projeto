from django.test import TestCase, Client
import json
from .observer import AgendamentoSubject, EmailNotifier, LogNotifier


class TestObserver(TestCase):

    def test_subject_notifica_todos_observers(self):
        resultados = []

        class TestNotifier(EmailNotifier):
            def update(self, agendamento):
                resultados.append(agendamento["cliente"])

        subject = AgendamentoSubject()
        subject.add_observer(TestNotifier())
        subject.notify({"cliente": "Gabriel", "data_hora": "2026-06-10 10:00"})

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0], "Gabriel")

    def test_email_notifier_executa_sem_erro(self):
        notifier = EmailNotifier()
        try:
            notifier.update({"cliente": "Gabriel", "data_hora": "2026-06-10 10:00"})
        except Exception as e:
            self.fail(f"EmailNotifier lançou exceção: {e}")

    def test_log_notifier_executa_sem_erro(self):
        notifier = LogNotifier()
        try:
            notifier.update({"cliente": "Gabriel", "data_hora": "2026-06-10 10:00"})
        except Exception as e:
            self.fail(f"LogNotifier lançou exceção: {e}")

    def test_subject_com_multiplos_observers(self):
        resultados = []

        class TestNotifier(LogNotifier):
            def update(self, agendamento):
                resultados.append(agendamento["cliente"])

        subject = AgendamentoSubject()
        subject.add_observer(TestNotifier())
        subject.add_observer(TestNotifier())
        subject.notify({"cliente": "Gabriel", "data_hora": "2026-06-10 10:00"})

        self.assertEqual(len(resultados), 2)


class TestNotificarView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_notificacao_valida_retorna_200(self):
        response = self.client.post(
            "/notificacoes/notificar/",
            data=json.dumps({"cliente": "Gabriel", "data_hora": "2026-06-10 10:00"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_nao_permitido(self):
        response = self.client.get("/notificacoes/notificar/")
        self.assertEqual(response.status_code, 405)
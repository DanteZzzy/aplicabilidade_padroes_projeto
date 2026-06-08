from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock

from agendamentos.models import Servico, Agendamento
from agendamentos.use_cases.criar_agendamento import CriarAgendamentoUseCase


class TestCriarAgendamento(TestCase):

    def setUp(self):
        self.corte = Servico.objects.create(
            nome="Corte Social",
            preco=Decimal("20.00"),
            tipo="corte"
        )
        self.barba = Servico.objects.create(
            nome="Barba Alinhada",
            preco=Decimal("15.00"),
            tipo="barba"
        )
        self.repository = MagicMock()
        self.use_case = CriarAgendamentoUseCase(repository=self.repository)

    def _data_futura(self, horas=24):
        return timezone.now() + timedelta(hours=horas)

    # ── TESTES DE DATA ──

    def test_agendamento_data_passada_retorna_erro(self):
        data_passada = timezone.now() - timedelta(hours=1)
        resultado = self.use_case.executar(
            cliente="Gabriel",
            data_agendada=data_passada,
            metodo_pagamento="pix",
            servicos=[self.corte]
        )
        self.assertEqual(resultado["status"], "erro")
        self.assertIn("passou", resultado["mensagem"])

    def test_agendamento_horario_duplicado_retorna_erro(self):
        self.repository.verificar_horario_existente.return_value = True
        resultado = self.use_case.executar(
            cliente="Gabriel",
            data_agendada=self._data_futura(),
            metodo_pagamento="pix",
            servicos=[self.corte]
        )
        self.assertEqual(resultado["status"], "erro")
        self.assertIn("reservado", resultado["mensagem"])

    # ── TESTES DE SERVIÇO ──

    def test_agendamento_sem_servico_retorna_erro(self):
        self.repository.verificar_horario_existente.return_value = False
        resultado = self.use_case.executar(
            cliente="Gabriel",
            data_agendada=self._data_futura(),
            metodo_pagamento="pix",
            servicos=[]
        )
        self.assertEqual(resultado["status"], "erro")
        self.assertIn("serviço", resultado["mensagem"])

    # ── TESTES DE PAGAMENTO ──

    def test_pagamento_invalido_retorna_erro(self):
        self.repository.verificar_horario_existente.return_value = False
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = {
                "status": "erro",
                "mensagem": "Forma de pagamento inválida."
            }
            resultado = self.use_case.executar(
                cliente="Gabriel",
                data_agendada=self._data_futura(),
                metodo_pagamento="boleto",
                servicos=[self.corte]
            )
        self.assertEqual(resultado["status"], "erro")

    def test_servico_pagamento_indisponivel_retorna_erro(self):
        self.repository.verificar_horario_existente.return_value = False
        with patch("requests.post", side_effect=Exception("conexão recusada")):
            resultado = self.use_case.executar(
                cliente="Gabriel",
                data_agendada=self._data_futura(),
                metodo_pagamento="pix",
                servicos=[self.corte]
            )
        self.assertEqual(resultado["status"], "erro")
        self.assertIn("indisponível", resultado["mensagem"])

    # ── TESTE DE SUCESSO ──

    def test_agendamento_valido_retorna_sucesso(self):
        self.repository.verificar_horario_existente.return_value = False
        self.repository.salvar_agendamento.return_value = MagicMock(cliente="Gabriel")

        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = {
                "status": "sucesso",
                "valor_final": "20.00",
                "mensagem": "Pagamento via PIX confirmado. Total: R$ 20.00"
            }
            resultado = self.use_case.executar(
                cliente="Gabriel",
                data_agendada=self._data_futura(),
                metodo_pagamento="pix",
                servicos=[self.corte]
            )
        self.assertEqual(resultado["status"], "sucesso")
        self.assertIn("Gabriel", resultado["mensagem"])


class TestServiceFactory(TestCase):

    def test_criar_corte_cria_servico_no_banco(self):
        from agendamentos.infrastructure.factory import ServiceFactory
        ServiceFactory.criar("corte", "Corte Teste", 30.00)
        self.assertTrue(Servico.objects.filter(nome="Corte Teste").exists())

    def test_criar_barba_cria_servico_no_banco(self):
        from agendamentos.infrastructure.factory import ServiceFactory
        ServiceFactory.criar("barba", "Barba Teste", 20.00)
        self.assertTrue(Servico.objects.filter(nome="Barba Teste").exists())

    def test_tipo_invalido_lanca_erro(self):
        from agendamentos.infrastructure.factory import ServiceFactory
        with self.assertRaises(ValueError):
            ServiceFactory.criar("sobrancelha", "Teste", 10.00)

    def test_criar_servicos_padrao_nao_duplica(self):
        from agendamentos.infrastructure.factory import ServiceFactory
        ServiceFactory.criar_servicos_padrao()
        ServiceFactory.criar_servicos_padrao()
        self.assertEqual(Servico.objects.filter(nome="Corte Social").count(), 1)
from django.test import TestCase, Client
from decimal import Decimal
import json
from .strategy import PixPayment, CartaoPayment


class TestPaymentStrategy(TestCase):

    def test_pix_retorna_sucesso(self):
        resultado = PixPayment().pagar(Decimal("100.00"))
        self.assertEqual(resultado["status"], "sucesso")

    def test_pix_retorna_valor_correto(self):
        resultado = PixPayment().pagar(Decimal("100.00"))
        self.assertEqual(resultado["valor_final"], "100.00")

    def test_cartao_retorna_sucesso(self):
        resultado = CartaoPayment().pagar(Decimal("100.00"))
        self.assertEqual(resultado["status"], "sucesso")

    def test_cartao_retorna_valor_correto(self):
        resultado = CartaoPayment().pagar(Decimal("100.00"))
        self.assertEqual(resultado["valor_final"], "100.00")


class TestProcessarPagamentoView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pagamento_pix_retorna_200(self):
        response = self.client.post(
            "/pagamentos/processar/",
            data=json.dumps({"metodo_pagamento": "pix", "valor": "100.00"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_pagamento_cartao_retorna_200(self):
        response = self.client.post(
            "/pagamentos/processar/",
            data=json.dumps({"metodo_pagamento": "cartao", "valor": "100.00"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_pagamento_invalido_retorna_400(self):
        response = self.client.post(
            "/pagamentos/processar/",
            data=json.dumps({"metodo_pagamento": "boleto", "valor": "100.00"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_get_nao_permitido(self):
        response = self.client.get("/pagamentos/processar/")
        self.assertEqual(response.status_code, 405)
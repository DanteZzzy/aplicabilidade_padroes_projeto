from decimal import Decimal
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def pagar(self, valor: Decimal):
        pass


class PixPayment(PaymentStrategy):

    def pagar(self, valor: Decimal):
        return {
            "status": "sucesso",
            "valor_final": str(round(valor, 2)),
            "mensagem": f"Pagamento via PIX confirmado. Total: R$ {valor:.2f}"
        }


class CartaoPayment(PaymentStrategy):

    def pagar(self, valor: Decimal):
        return {
            "status": "sucesso",
            "valor_final": str(round(valor, 2)),
            "mensagem": f"Pagamento via Cartão confirmado. Total: R$ {valor:.2f}"
        }
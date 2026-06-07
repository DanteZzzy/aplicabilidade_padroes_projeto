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
            "valor_final": valor,
            "mensagem": f"Pagamento Realizado via PIX de R$ {valor:.2f}."
        }

class CartaoPayment(PaymentStrategy):
    def pagar(self, valor: Decimal):
        return {
            "status": "sucesso",
            "valor_final": valor,
            "mensagem": f"Pagamento Realizado via Cartão de R$ {valor:.2f}."
        }
from decimal import Decimal


class PaymentStrategy:

    def pagar(self, valor):
        raise NotImplementedError


class PixPayment(PaymentStrategy):

    def pagar(self, valor):

        valor_final = valor * Decimal("0.90")

        return {
            "status": "sucesso",
            "valor_final": round(valor_final, 2),
            "mensagem": f"Pagamento PIX aprovado com 10% de desconto. Total: R$ {valor_final:.2f}"
        }


class CartaoPayment(PaymentStrategy):

    def pagar(self, valor):

        valor_final = valor * Decimal("1.05")

        return {
            "status": "sucesso",
            "valor_final": round(valor_final, 2),
            "mensagem": f"Pagamento no cartão aprovado com taxa de 5%. Total: R$ {valor_final:.2f}"
        }
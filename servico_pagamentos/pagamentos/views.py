from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from decimal import Decimal
import json
from .strategy import PixPayment, CartaoPayment

PAYMENT_STRATEGIES = {
    "pix": PixPayment,
    "cartao": CartaoPayment,
}

@csrf_exempt
@require_POST
def processar_pagamento(request):
    try:
        data = json.loads(request.body)
        metodo = data.get("metodo_pagamento")
        valor = Decimal(str(data.get("valor", 0)))

        strategy_class = PAYMENT_STRATEGIES.get(metodo)
        if not strategy_class:
            return JsonResponse({"status": "erro", "mensagem": "Forma de pagamento inválida."}, status=400)

        resultado = strategy_class().pagar(valor)
        return JsonResponse(resultado)

    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)
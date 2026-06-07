from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .observer import AgendamentoSubject, EmailNotifier, LogNotifier


@csrf_exempt
@require_POST
def notificar(request):
    try:
        data = json.loads(request.body)
        cliente = data.get("cliente")
        data_hora = data.get("data_hora")

        subject = AgendamentoSubject()
        subject.add_observer(EmailNotifier())
        subject.add_observer(LogNotifier())
        subject.notify({"cliente": cliente, "data_hora": data_hora})

        return JsonResponse({"status": "sucesso", "mensagem": "Notificações enviadas."})

    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)
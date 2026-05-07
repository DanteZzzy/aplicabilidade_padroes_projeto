from django.shortcuts import render

from .models import Agendamento, Servico

from .services.facade import AgendamentoFacade
from .services.factory import ServiceFactory


def criar_agendamento(request):

    # FACTORY
    ServiceFactory.criar_servicos_padrao()

    mensagem = None
    erro = None
    pagamento_msg = None

    if request.method == "POST":

        cliente = request.POST.get("cliente")

        corte_id = request.POST.get("corte")

        barba_id = request.POST.get("barba")

        metodo_pagamento = request.POST.get("pagamento")

        # Junta os serviços escolhidos
        servicos_ids = []

        if corte_id:
            servicos_ids.append(corte_id)

        if barba_id:
            servicos_ids.append(barba_id)

        # VALIDAÇÕES
        if not cliente or cliente.strip() == "":

            erro = "Digite o nome do cliente."

        elif not servicos_ids:

            erro = "Selecione ao menos um serviço."

        elif not metodo_pagamento:

            erro = "Selecione uma forma de pagamento."

        else:

            servicos = Servico.objects.filter(id__in=servicos_ids)

            facade = AgendamentoFacade()

            resultado = facade.criar_agendamento(
                cliente=cliente,
                servicos=servicos,
                metodo_pagamento=metodo_pagamento
            )

            if resultado["status"] == "sucesso":

                mensagem = resultado["mensagem"]

                pagamento_msg = resultado["pagamento_msg"]

            else:

                erro = resultado["mensagem"]

    agendamentos = Agendamento.objects.all().order_by('-data')

    servicos_corte = Servico.objects.filter(tipo="corte")

    servicos_barba = Servico.objects.filter(tipo="barba")

    return render(request, "agendamentos/agendar.html", {

        "mensagem": mensagem,

        "erro": erro,

        "pagamento_msg": pagamento_msg,

        "agendamentos": agendamentos,

        "servicos_corte": servicos_corte,

        "servicos_barba": servicos_barba

    })
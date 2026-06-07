from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .models import Agendamento, Servico
from agendamentos.infrastructure.factory import ServiceFactory
from agendamentos.infrastructure.repositories import DjangoAgendamentoRepository
from agendamentos.use_cases.criar_agendamento import CriarAgendamentoUseCase


def criar_agendamento(request):
    ServiceFactory.criar_servicos_padrao()

    if request.method == "POST":
        cliente = request.POST.get("cliente")
        data_str = request.POST.get("data_agendada")
        metodo_pagamento = request.POST.get("pagamento")

        corte_id = request.POST.get("corte")
        barba_id = request.POST.get("barba")

        servicos_ids = [sid for sid in [corte_id, barba_id] if sid]

        erros = []
        if not cliente or cliente.strip() == "":
            erros.append("Digite o nome do cliente.")
        if not data_str:
            erros.append("Selecione uma data e horário.")
        if not metodo_pagamento:
            erros.append("Selecione uma forma de pagamento.")
        if not servicos_ids:
            erros.append("Selecione ao menos um serviço (Corte ou Barba).")

        if erros:
            messages.error(request, " | ".join(erros))
        else:
            try:
                data_agendada = datetime.strptime(data_str, "%Y-%m-%dT%H:%M")
                data_agendada = timezone.make_aware(data_agendada)

                servicos_selecionados = list(Servico.objects.filter(id__in=servicos_ids))

                repositorio = DjangoAgendamentoRepository()
                use_case = CriarAgendamentoUseCase(repository=repositorio)

                resultado = use_case.executar(
                    cliente=cliente,
                    data_agendada=data_agendada,
                    metodo_pagamento=metodo_pagamento,
                    servicos=servicos_selecionados
                )

                if resultado["status"] == "sucesso":
                    messages.success(request, f"{resultado['mensagem']} | {resultado['pagamento_msg']}")
                    return redirect(request.path)
                else:
                    messages.error(request, resultado["mensagem"])

            except ValueError:
                messages.error(request, "Data e horário inválidos.")

    agendamentos = Agendamento.objects.all().order_by('-data_hora')
    servicos_corte = Servico.objects.filter(tipo="corte")
    servicos_barba = Servico.objects.filter(tipo="barba")

    return render(request, "agendamentos/agendar.html", {
        "agendamentos": agendamentos,
        "servicos_corte": servicos_corte,
        "servicos_barba": servicos_barba,
    })
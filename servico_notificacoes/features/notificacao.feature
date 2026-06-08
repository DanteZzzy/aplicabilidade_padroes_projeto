# language: pt

Funcionalidade: Notificação de agendamentos
  Como o serviço de agendamentos
  Quero notificar sobre novos agendamentos
  Para manter o registro e comunicar o cliente

  Cenário: Notificação enviada com sucesso
    Dado que um agendamento foi criado para "Gabriel"
    E a data do agendamento é "2026-06-10 10:00"
    Quando a notificação for disparada
    Então todos os observers devem ser notificados

  Cenário: Múltiplos observers recebem a notificação
    Dado que um agendamento foi criado para "Gabriel"
    E a data do agendamento é "2026-06-10 10:00"
    E existem 2 observers registrados
    Quando a notificação for disparada
    Então todos os observers devem ser notificados
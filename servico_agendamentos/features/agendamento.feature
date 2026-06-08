# language: pt

Funcionalidade: Agendamento de serviços na barbearia
  Como um cliente da barbearia
  Quero agendar um horário
  Para garantir meu atendimento

  Cenário: Agendamento realizado com sucesso
    Dado que o cliente "Gabriel" quer agendar para daqui 24 horas
    E escolheu o serviço "Corte Social" por R$ 20.00
    E selecionou pagamento via "pix"
    Quando o agendamento for confirmado
    Então o resultado deve ser "sucesso"

  Cenário: Agendamento para data no passado
    Dado que o cliente "Gabriel" quer agendar para 1 hora atrás
    E escolheu o serviço "Corte Social" por R$ 20.00
    E selecionou pagamento via "pix"
    Quando o agendamento for confirmado
    Então o resultado deve ser "erro"
    E a mensagem deve conter "passou"

  Cenário: Agendamento sem serviço selecionado
    Dado que o cliente "Gabriel" quer agendar para daqui 24 horas
    E não selecionou nenhum serviço
    E selecionou pagamento via "pix"
    Quando o agendamento for confirmado
    Então o resultado deve ser "erro"
    E a mensagem deve conter "serviço"

  Cenário: Horário já reservado
    Dado que o cliente "Gabriel" quer agendar para daqui 24 horas
    E escolheu o serviço "Corte Social" por R$ 20.00
    E selecionou pagamento via "pix"
    E o horário já está reservado
    Quando o agendamento for confirmado
    Então o resultado deve ser "erro"
    E a mensagem deve conter "reservado"
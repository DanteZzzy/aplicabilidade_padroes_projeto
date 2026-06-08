# language: pt

Funcionalidade: Processamento de pagamentos
  Como o serviço de agendamentos
  Quero processar pagamentos
  Para confirmar o agendamento do cliente

  Cenário: Pagamento via PIX realizado com sucesso
    Dado que o valor do serviço é R$ 100.00
    E o método de pagamento é "pix"
    Quando o pagamento for processado
    Então o status do pagamento deve ser "sucesso"

  Cenário: Pagamento via cartão realizado com sucesso
    Dado que o valor do serviço é R$ 100.00
    E o método de pagamento é "cartao"
    Quando o pagamento for processado
    Então o status do pagamento deve ser "sucesso"

  Cenário: Método de pagamento inválido
    Dado que o valor do serviço é R$ 100.00
    E o método de pagamento é "boleto"
    Quando o pagamento for processado
    Então o status do pagamento deve ser "erro"
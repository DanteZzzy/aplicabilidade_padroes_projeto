# 📅 Sistema de Agendamento — Barbearia

## 📋 Descrição do Problema

Barbearias tradicionais enfrentam dificuldades no gerenciamento de agendamentos: clientes ligam ou aparecem sem hora marcada, gerando filas, conflitos de horário e perda de clientes. A ausência de um sistema centralizado também dificulta o controle financeiro, já que diferentes formas de pagamento são aceitas sem registro adequado.

**Proposta de solução:** um sistema web que permite ao cliente agendar seu horário online, escolher os serviços desejados (corte e/ou barba), selecionar a forma de pagamento e receber confirmação automática. O sistema valida conflitos de horário, calcula o valor final automaticamente e notifica o estabelecimento a cada novo agendamento — tudo isso distribuído em microsserviços independentes, garantindo escalabilidade e manutenibilidade.

---

## 🔗 Acesso ao sistema

> **https://servico-agendamentos.onrender.com**

⚠️ **Atenção — plano gratuito do Render (spin down):**
O sistema está hospedado gratuitamente. Após 15 minutos de inatividade, cada serviço "dorme" e precisa ser acordado manualmente. Caso apareça a mensagem **"Serviço de pagamento indisponível"**, siga os passos abaixo:

**1.** Acesse os links abaixo em abas separadas do navegador para acordar os serviços (vai aparecer uma mensagem de erro de método — isso é normal):
- https://servico-pagamentos.onrender.com/pagamentos/processar/
- https://servico-notificacoes.onrender.com/notificacoes/notificar/

**2.** Aguarde alguns segundos e tente realizar o agendamento novamente.

---

## 🚀 Tecnologias utilizadas

- Python 3.11
- Django 5.2
- SQLite
- Docker / Docker Compose
- Gunicorn
- Whitenoise
- Behave (BDD)
- Pytest / Django Test (TDD)
- Requests
- Render (deploy)

---

## 🏗️ Arquitetura — Microsserviços

O sistema é dividido em 3 microsserviços independentes, cada um com seu próprio container Docker:

| Serviço | Responsabilidade | Porta |
|---|---|---|
| `servico_agendamentos` | Interface principal, regras de negócio, banco de dados | 8000 |
| `servico_pagamentos` | Processamento de pagamentos (Strategy) | 8001 |
| `servico_notificacoes` | Notificações por e-mail e log (Observer) | 8002 |

A comunicação entre os serviços é feita via HTTP usando a biblioteca `requests`. O `servico_agendamentos` orquestra o fluxo chamando os outros dois serviços após validar os dados do agendamento.

---

## 🧼 Arquitetura Limpa

O `servico_agendamentos` segue os princípios da Arquitetura Limpa, com separação clara de camadas:

```bash
agendamentos/
├── domain/
│   └── repositories.py       ← interfaces abstratas (contratos)
├── infrastructure/
│   ├── repositories.py       ← implementação concreta com Django ORM
│   └── factory.py            ← criação de entidades
└── use_cases/
├── criar_agendamento.py  ← orquestra o fluxo de negócio
├── observer.py           ← padrão Observer
└── strategy.py           ← padrão Strategy
```

---

## 🧠 Padrões de Projeto Utilizados

### 🏗️ Facade
O `CriarAgendamentoUseCase` centraliza toda a lógica de criação de agendamentos, escondendo a complexidade do processo atrás de uma única chamada. A `views.py` não conhece os detalhes de pagamento, notificação ou persistência — apenas chama o use case e recebe o resultado.

Responsável por:
- Validar regras de negócio (data no passado, horário duplicado, serviço obrigatório)
- Chamar o microsserviço de pagamento
- Persistir o agendamento via repositório
- Chamar o microsserviço de notificação

### 🏭 Factory
Centraliza a criação dos serviços disponíveis na barbearia em `infrastructure/factory.py`. Usa classes especializadas `CorteFactory` e `BarbaFactory` que herdam de `ServicoFactory` (ABC). Para adicionar um novo tipo de serviço, basta criar uma nova classe e registrá-la no dicionário `FACTORIES` — sem modificar a lógica existente (Open/Closed).

### 💳 Strategy
Define comportamentos de pagamento intercambiáveis em `servico_pagamentos/pagamentos/strategy.py`. As classes `PixPayment` e `CartaoPayment` implementam a interface abstrata `PaymentStrategy`. A troca de comportamento ocorre em tempo de execução conforme o método escolhido pelo cliente.

### 🔔 Observer
Notifica automaticamente após a criação de um agendamento em `servico_notificacoes/notificacoes/observer.py`. O `AgendamentoSubject` mantém uma lista de observers e os notifica todos. `EmailNotifier` e `LogNotifier` são implementações concretas — adicionar um novo tipo de notificação não exige modificar o código existente.

---

## ✅ Princípios SOLID aplicados

| Princípio | Onde |
|---|---|
| S — Single Responsibility | Cada classe tem uma única responsabilidade (`CorteFactory` só cria cortes, `EmailNotifier` só notifica por e-mail) |
| O — Open/Closed | `FACTORIES` e `PAYMENT_STRATEGIES` usam dicionários para extensão sem modificação |
| L — Liskov Substitution | `PixPayment` e `CartaoPayment` substituem `PaymentStrategy` sem quebrar o sistema |
| I — Interface Segregation | Interfaces pequenas e específicas (`PaymentStrategy`, `Observer`, `Subject`) |
| D — Dependency Inversion | `CriarAgendamentoUseCase` depende de `AgendamentoRepositoryInterface`, não da implementação concreta |

---

## 🧹 Evidências de Clean Code

- Nomes descritivos e autoexplicativos em todas as classes e métodos
- Funções pequenas com responsabilidade única
- Separação clara entre camadas (views não contém lógica de negócio)
- Validações centralizadas no use case
- Sem código duplicado (uso de `get_or_create` para evitar duplicação no banco)
- Comentários apenas onde necessário

---

## 🧪 TDD — Testes

Os testes foram escritos seguindo o ciclo Red → Green → Refactor.

### Rodar os testes:
```bash
docker-compose exec agendamentos python manage.py test agendamentos
docker-compose exec pagamentos python manage.py test pagamentos
docker-compose exec notificacoes python manage.py test notificacoes
```

### Resultado da execução:

```bash
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
Ran 10 tests in 0.035s
OK
Destroying test database for alias 'default'...
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
Ran 8 tests in 0.023s
OK
Destroying test database for alias 'default'...
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.[EMAIL] Enviado para Gabriel
[LOG] Agendamento criado para Gabriel em 2026-06-10 10:00
.[EMAIL] Enviado para Gabriel
.[LOG] Agendamento criado para Gabriel em 2026-06-10 10:00
...
Ran 6 tests in 0.018s
OK
Destroying test database for alias 'default'...
```

### Cobertura:

| Serviço | Testes | Casos cobertos |
|---|---|---|
| agendamentos | 10 | Data no passado, horário duplicado, sem serviço, pagamento inválido, serviço indisponível, sucesso, factory |
| pagamentos | 8 | PIX, cartão, método inválido, GET não permitido |
| notificacoes | 6 | Observer único, múltiplos observers, view de notificação |

---

## 🥒 BDD — Comportamento

Cenários escritos em português usando Behave.

### Rodar os cenários:
```bash
docker-compose exec agendamentos python -m behave features/
docker-compose exec pagamentos python -m behave features/
docker-compose exec notificacoes python -m behave features/
```

### Resultado da execução:
```bash
Funcionalidade: Agendamento de serviços na barbearia
Cenário: Agendamento realizado com sucesso
Dado que o cliente "Gabriel" quer agendar para daqui 24 horas
E escolheu o serviço "Corte Social" por R$ 20.00
E selecionou pagamento via "pix"
Quando o agendamento for confirmado
Então o resultado deve ser "sucesso"
Cenário: Agendamento para data no passado
Cenário: Agendamento sem serviço selecionado
Cenário: Horário já reservado
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
24 steps passed, 0 failed, 0 skipped

Funcionalidade: Processamento de pagamentos
Cenário: Pagamento via PIX realizado com sucesso
Cenário: Pagamento via cartão realizado com sucesso
Cenário: Método de pagamento inválido
1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
12 steps passed, 0 failed, 0 skipped

Funcionalidade: Notificação de agendamentos
Cenário: Notificação enviada com sucesso
Cenário: Múltiplos observers recebem a notificação
1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
9 steps passed, 0 failed, 0 skipped
```

### Cobertura:

| Serviço | Cenários | Descrição |
|---|---|---|
| agendamentos | 4 | Sucesso, data no passado, sem serviço, horário reservado |
| pagamentos | 3 | PIX, cartão, método inválido |
| notificacoes | 2 | Observer único, múltiplos observers |

---

## 🐳 Docker

O projeto usa Docker Compose para orquestrar os 3 microsserviços.

### Rodar o projeto localmente:
```bash
docker-compose up --build
```

### Acessar:
http://localhost:8000

---

## ⚙️ Como rodar sem Docker

### 1. Clonar o repositório
```bash
git clone https://github.com/DanteZzzy/aplicabilidade_padroes_projeto.git
cd agendamento_system/servico_agendamentos
```

### 2. Criar ambiente virtual
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar migrations
```bash
python manage.py migrate
```

### 5. Rodar o servidor
```bash
python manage.py runserver
```

### Acessar:
http://127.0.0.1:8000
http://127.0.0.1:8000/admin

---

## 🗄️ Banco de dados

O sistema utiliza SQLite por padrão. Em produção os dados não são persistentes entre redeploys (limitação do plano gratuito do Render).

### Apagar agendamentos (mantém serviços):
```bash
python manage.py shell -c "from agendamentos.models import Agendamento; Agendamento.objects.all().delete()"
```

### Apagar serviços:
```bash
python manage.py shell -c "from agendamentos.models import Servico; Servico.objects.all().delete()"
```

### Resetar banco:
```bash
python manage.py flush
```

> ⚠️ Atenção: esse comando apaga todos os dados cadastrados, incluindo serviços e agendamentos.

---

## 📁 Estrutura do Projeto
```bash
agendamento_system/
│
├── servico_agendamentos/
│   ├── agendamento_system/       ← configurações Django
│   ├── agendamentos/
│   │   ├── domain/
│   │   │   └── repositories.py
│   │   ├── infrastructure/
│   │   │   ├── factory.py
│   │   │   └── repositories.py
│   │   ├── use_cases/
│   │   │   ├── criar_agendamento.py
│   │   │   ├── observer.py
│   │   │   └── strategy.py
│   │   ├── templates/
│   │   ├── static/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── tests.py
│   ├── features/                 ← BDD
│   ├── Dockerfile
│   └── requirements.txt
│
├── servico_pagamentos/
│   ├── core/
│   ├── pagamentos/
│   │   ├── strategy.py
│   │   ├── views.py
│   │   └── tests.py
│   ├── features/                 ← BDD
│   ├── Dockerfile
│   └── requirements.txt
│
├── servico_notificacoes/
│   ├── core/
│   ├── notificacoes/
│   │   ├── observer.py
│   │   ├── views.py
│   │   └── tests.py
│   ├── features/                 ← BDD
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## 🔍 Justificativa Técnica

### Por que Django?
Django oferece ORM robusto, admin integrado, sistema de migrations e estrutura MVC bem definida — ideal para um sistema de agendamentos com banco de dados relacional.

### Por que microsserviços?
A separação em microsserviços permite que cada responsabilidade evolua independentemente. O serviço de pagamentos pode ser substituído por uma integração real (Stripe, PagSeguro) sem afetar o restante do sistema. O serviço de notificações pode passar a enviar e-mails reais sem tocar na lógica de agendamento.

### Por que SQLite?
Simplicidade para desenvolvimento e avaliação acadêmica. Em produção real seria substituído por PostgreSQL com volume persistente.

### Por que Docker?
Garante que o ambiente de execução seja idêntico em qualquer máquina, eliminando problemas de dependências. O Docker Compose orquestra os 3 serviços com um único comando.

### Por que Render?
Plataforma gratuita com suporte a Docker, deploy automático via GitHub e HTTPS nativo — ideal para projetos acadêmicos.

### Por que Behave para BDD?
Permite escrever cenários em português, aproximando a documentação do negócio real e facilitando a compreensão por parte de não-desenvolvedores.

### Por que Arquitetura Limpa?
A separação em camadas (domain, use_cases, infrastructure) garante que as regras de negócio não dependam de frameworks ou banco de dados. O `CriarAgendamentoUseCase` pode ser testado sem Django, sem banco e sem HTTP.

---

## 👨‍💻 Autor: Gabriel Teixeira de Faria
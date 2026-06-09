# 📅 Sistema de Agendamento — Barbearia

Sistema web desenvolvido com Django para gerenciamento de agendamentos de serviços de uma barbearia, com suporte a diferentes métodos de pagamento e aplicação de padrões de projeto, arquitetura limpa, microsserviços e boas práticas de engenharia de software.

---

## 🔗 Acesso ao sistema

> https://servico-agendamentos.onrender.com

⚠️ O sistema está hospedado no plano gratuito do Render. Na primeira requisição após um período de inatividade, os serviços podem demorar até 60 segundos para responder (spin down). Aguarde e tente novamente caso ocorra erro de pagamento indisponível.

---

## 🚀 Tecnologias utilizadas

- Python 3.11
- Django 5.2
- SQLite
- Docker / Docker Compose
- Gunicorn
- Whitenoise
- Behave (BDD)
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
Centraliza a lógica de criação de agendamentos no `CriarAgendamentoUseCase`, escondendo a complexidade do processo atrás de uma única chamada. A `views.py` não conhece os detalhes de pagamento, notificação ou persistência.

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

---

## 👨‍💻 Autor: Gabriel Teixeira de Faria
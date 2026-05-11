# 📅 Sistema de Agendamento

Sistema web desenvolvido com Django para gerenciamento de agendamentos de serviços de uma barbearia, com suporte a diferentes métodos de pagamento e aplicação de padrões de projeto.

---

## 🚀 Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML/CSS

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/DanteZzzy/aplicabilidade_padroes_projeto.git
cd agendamento_system
```

### 2. Criar ambiente virtual
```bash
# Criar ambiente
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuário
```bash
python manage.py createsuperuser
```

### 6. Rodar o servidor
```bash
python manage.py runserver
```

### Para acessar use:
- Para agendar serviço
http://127.0.0.1:8000/agendar/
- Para editar e configurar os serviços
http://127.0.0.1:8000/admin/



## 🗄️ Banco de dados

O sistema utiliza SQLite por padrão.

#### Apagar só os agendamentos (mantém os serviços):
```bash
python manage.py shell -c "from agendamentos.models import Agendamento; Agendamento.objects.all().delete()"
```
#### Apagar só os serviços:
```bash
python manage.py shell -c "from agendamentos.models import Servico; Servico.objects.all().delete()"
```
#### Resetar banco:
```bash
python manage.py flush
```

> ⚠️ Atenção: esse comando apaga todos os dados cadastrados, incluindo serviços e agendamentos.

---

## 📌 Funcionalidades

- Cadastro de agendamentos com nome do cliente
- Seleção de serviços de corte e/ou barba
- Pagamento via Pix (10% de desconto) ou Cartão (5% de taxa)
- Cálculo automático do valor final
- Notificação por e-mail e log após agendamento
- Listagem de agendamentos realizados



## 🧠 Padrões de Projeto Utilizados

### 🏗️ Facade
Centraliza a lógica de criação de agendamentos, escondendo a complexidade do processo atrás de uma única chamada.


Responsável por:
- Calcular o valor total dos serviços
- Aplicar a estratégia de pagamento
- Criar o agendamento no banco
- Notificar os observers

---

### 🏭 Factory
Centraliza a criação dos serviços disponíveis na barbearia, evitando duplicações no banco de dados.
services/factory.py
Implementações:
- `criar_corte(nome, preco)` — cria um serviço do tipo corte
- `criar_barba(nome, preco)` — cria um serviço do tipo barba
- `criar_servicos_padrao()` — popula os serviços iniciais automaticamente

---

### 💳 Strategy
Define diferentes comportamentos de pagamento de forma intercambiável.
services/strategy.py
Implementações:
- `PixPayment` — aplica 10% de desconto
- `CartaoPayment` — aplica 5% de taxa

Permite trocar o comportamento de pagamento dinamicamente em tempo de execução.

---

### 🔔 Observer
Notifica os interessados automaticamente após a criação de um agendamento.
services/observer.py
Implementações:
- `EmailNotifier` — simula envio de e-mail ao cliente
- `LogNotifier` — registra o agendamento no log do sistema


## 📁 Estrutura do Projeto
```bash
agendamento_system/
│
├── agendamento_system/
│   ├── settings.py
│   ├── urls.py
│
├── agendamentos/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── services/
│   │   ├── facade.py
│   │   ├── factory.py
│   │   ├── strategy.py
│   │   └── observer.py
│   │
│   ├── templates/
│   │   └── agendamentos/
│   │       └── agendar.html
│   │
│   └── static/
│       └── agendamentos/
│           └── style.css
│
├── requirements.txt
├── db.sqlite3
└── manage.py
```


## 👨‍💻 Autor: Gabriel Teixeira de Faria
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
git clone <url-do-repositorio>
cd agendamento_system
```

### 2. Criar ambiente virtual
```bash
# Criar ambiente
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate

#No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install django
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

```bash
# Para Agendar Serviço
http://127.0.0.1:8000
# Para Editar e Configurar os serviços
http://127.0.0.1:8000/admin
```

### 🗄️ Banco de dados

O sistema utiliza SQLite por padrão.

#### Resetar banco:
```bash
python manage.py flush
```

#### Atenção: Utilizar esse comando irá apagar todos os dados cadastrados, desde os serviços inseridos e os agendamentos feitos.

### 📌 Funcionalidades
- Cadastro de agendamentos
- Seleção de serviços
- Escolha de método de pagamento (Pix ou Cartão)
- Listagem de agendamentos
- Interface simples e funcional

### 🧠 Padrões de Projeto Utilizados
### 🏗️ Facade

Centraliza a lógica de criação de agendamentos.
```bash
# Arquivo
services/facade.py
```
Responsável por:

- Criar agendamento
- Aplicar pagamento
- Notificar eventos

### 💳 Strategy

Define diferentes formas de pagamento.

```bash
# Arquivo
services/strategy.py
```
Implementações:

- PixPayment
- CartaoPayment

Permite trocar o comportamento de pagamento dinamicamente.

### 🔔 Observer

Notifica ações após o agendamento.
```bash
# Arquivo
services/observer.py
```

Exemplos:

- EmailNotifier
- LogNotifier

### 📁 Estrutura do Projeto
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
│   │   ├── strategy.py
│   │   ├── observer.py
│   │   ├── factory.py
│   │
│   ├── templates/
│   │   └── agendamentos/
│   │       └── agendar.html
│   │
│   ├── static/
│       └── agendamentos/
│           └── style.css   
│
├── db.sqlite3
├── manage.py
```

### 👨‍💻 Autor: Gabriel Teixeira de Faria


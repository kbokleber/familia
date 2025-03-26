# Sistema de Gestão de Manutenção Residencial

Uma plataforma web para gerenciamento de manutenções residenciais, desenvolvida com Django e Bootstrap 5.

## Funcionalidades

- Autenticação de usuários
- Gestão de equipamentos e veículos
- Ordens de serviço
- Dashboard interativo
- Histórico de manutenções
- Notificações
- Interface responsiva

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Virtualenv

## Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd [nome-do-diretorio]
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## Uso

1. Acesse http://localhost:8000 no navegador
2. Faça login com suas credenciais
3. Comece a gerenciar suas manutenções!

## Estrutura do Projeto

- `maintenance/` - Aplicação principal
- `accounts/` - Gestão de usuários
- `dashboard/` - Dashboard e relatórios
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `templates/` - Templates HTML

## Tecnologias Utilizadas

- Backend: Django
- Frontend: Bootstrap 5
- Banco de Dados: SQLite3
- Gráficos: Plotly
- Notificações: Django Notifications 
# Use uma imagem base do Python
FROM python:3.12-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Argumento de build para a versão
ARG VERSION
ENV VERSION=$VERSION

# Defina o diretório de trabalho
WORKDIR /app

# Instale o cliente do PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instale as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o projeto
COPY . .

# Exponha a porta 8001
EXPOSE 8001

# Comando para executar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"] 
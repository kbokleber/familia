# Use uma imagem base mais leve
FROM python:3.11-slim

# Defina variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=maintenance_project.settings_prod

# Crie e defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o projeto
COPY . .

# Crie um usuário não-root
RUN useradd -m app_user && \
    chown -R app_user:app_user /app

# Mude para o usuário não-root
USER app_user

# Crie diretórios necessários com permissões corretas
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R app_user:app_user /app/staticfiles /app/media

# Exponha a porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "maintenance_project.wsgi:application"] 
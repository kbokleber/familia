# Use uma imagem base mais leve
FROM python:3.12-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=maintenance_project.settings_prod

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
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copie o projeto
COPY . .

# Crie um usuário não-root
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Mude para o usuário não-root
USER appuser

# Crie diretórios necessários com permissões corretas
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

# Torna o script de entrada executável
RUN chmod +x /app/entrypoint.sh

# Define o script de entrada como ponto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Exponha a porta
EXPOSE 8000

# Comando padrão
CMD ["gunicorn", "maintenance_project.wsgi:application", "--config", "gunicorn.conf.py"] 
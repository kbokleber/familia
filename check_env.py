import os

env_vars = [
    'DB_NAME',
    'POSTGRES_DB',
    'DB_USER',
    'POSTGRES_USER',
    'DB_PASSWORD',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_HOST',
    'DB_PORT',
    'POSTGRES_PORT',
    'DJANGO_SETTINGS_MODULE',
    'DOCKER_CONTAINER'
]

print("Variáveis de ambiente encontradas:")
print("-" * 30)
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"{var}: {value}")
    else:
        print(f"{var}: não definida") 
import os
import sys
import subprocess
import venv
from pathlib import Path

def setup_virtual_env():
    """Cria e ativa o ambiente virtual"""
    venv_path = Path('.venv')
    if not venv_path.exists():
        print("Criando ambiente virtual...")
        venv.create('.venv', with_pip=True)
    
    # Determina o caminho do executável Python do ambiente virtual
    if sys.platform == 'win32':
        python_path = venv_path / 'Scripts' / 'python.exe'
    else:
        python_path = venv_path / 'bin' / 'python'
    
    return python_path

def install_requirements(python_path):
    """Instala as dependências do projeto"""
    print("Instalando dependências...")
    subprocess.run([str(python_path), '-m', 'pip', 'install', '-r', 'requirements.txt'])

def run_migrations(python_path):
    """Executa as migrações do banco de dados"""
    print("Executando migrações...")
    subprocess.run([str(python_path), 'manage.py', 'migrate', '--settings=maintenance_project.settings_dev'])

def collect_static(python_path):
    """Coleta arquivos estáticos"""
    print("Coletando arquivos estáticos...")
    subprocess.run([str(python_path), 'manage.py', 'collectstatic', '--noinput', '--settings=maintenance_project.settings_dev'])

def run_server(python_path):
    """Inicia o servidor de desenvolvimento"""
    print("Iniciando servidor de desenvolvimento...")
    subprocess.run([str(python_path), 'manage.py', 'runserver', '--settings=maintenance_project.settings_dev'])

def main():
    # Configura o ambiente virtual
    python_path = setup_virtual_env()
    
    # Instala as dependências
    install_requirements(python_path)
    
    # Executa as migrações
    run_migrations(python_path)
    
    # Coleta arquivos estáticos
    collect_static(python_path)
    
    # Inicia o servidor
    run_server(python_path)

if __name__ == '__main__':
    main() 
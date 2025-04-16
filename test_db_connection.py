import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def test_connection():
    try:
        # Parâmetros de conexão
        conn_params = {
            'dbname': os.getenv('DB_NAME', 'sistema_familiar_db'),
            'user': os.getenv('DB_USER', 'sistema_familiar_user'),
            'password': os.getenv('DB_PASSWORD', 'SuaSenhaSeguraParaDB2024'),
            'host': os.getenv('DB_HOST', '89.116.186.192'),
            'port': os.getenv('DB_PORT', '5440')
        }
        
        print("Tentando conectar ao banco de dados...")
        print(f"Host: {conn_params['host']}")
        print(f"Porta: {conn_params['port']}")
        print(f"Banco: {conn_params['dbname']}")
        print(f"Usuário: {conn_params['user']}")
        
        # Tenta estabelecer a conexão
        conn = psycopg2.connect(**conn_params)
        
        print("\nConexão estabelecida com sucesso!")
        
        # Testa uma query simples
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print(f"\nVersão do PostgreSQL: {version[0]}")
        
        # Fecha a conexão
        cur.close()
        conn.close()
        print("\nConexão fechada.")
        return True
        
    except Exception as e:
        print(f"\nErro ao conectar ao banco de dados: {str(e)}")
        return False

if __name__ == '__main__':
    test_connection() 
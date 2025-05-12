import psycopg2
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

@contextmanager
def get_db_connection():
    conn = None
    print(f"Host: {os.getenv('DB_HOST')}")
    print("\nTentando conectar com:")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Porta: {os.getenv('DB_PORT')}")
    print(f"Banco: {os.getenv('DB_NAME')}")
    print(f"Usuário: {os.getenv('DB_USER')}")
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host='34.55.29.245',#os.getenv('DB_HOST'),ARRUMAR!!!!!!!!!!!!!!!!!!!!!!!!!!!
            port=os.getenv('DB_PORT')
        )
        print("Conexão estabelecida com sucesso!")
        yield conn
    except psycopg2.OperationalError as e:
        print(f" Falha na conexão: {e}")
        raise
    finally:
        if conn:
            conn.close()
            print(" Conexão encerrada")

def test_db_conn():
    print("\n Iniciando teste de conexão...")
    print(f"Tentando conectar em: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                print(f" Versão do PostgreSQL: {db_version[0]}")
                
                # Teste adicional - Listar tabelas (deve retornar vazio)
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                print(f" Tabelas existentes: {[t[0] for t in cur.fetchall()]}")
                
        return True
    except Exception as e:
        print(f" Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    test_db_conn()
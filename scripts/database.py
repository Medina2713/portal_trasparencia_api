import psycopg2
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

@contextmanager
def get_db_connection():
    conn = None
    
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        print("\nConexão estabelecida com sucesso!\n")
        yield conn
    except psycopg2.OperationalError as e:
        print(f" Falha na conexão: {e}")
        raise
    finally:
        if conn:
            conn.close()
            

def test_db_conn():
    print("\n Iniciando teste de conexão...")
    print(f"Tentando conectar em: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                print(f" Versão do PostgreSQL: {db_version[0]}")
                
                #Listar tabelas
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


def create_tables():
   
    commands = (
        """
        CREATE TABLE IF NOT EXISTS municipio (
            codigo_ibge VARCHAR(20) PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            codigo_regiao VARCHAR(20),
            nome_regiao VARCHAR(50),
            uf_sigla CHAR(10),
            uf_nome VARCHAR(100),
            pais VARCHAR(100) DEFAULT 'Brasil',
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS beneficiario (
            nis VARCHAR(50) PRIMARY KEY,
            cpf VARCHAR(50),
            nome VARCHAR(300) NOT NULL,
            cpf_formatado VARCHAR(50),
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS saque (
            id SERIAL PRIMARY KEY,
            id_original BIGINT,
            data_mes_competencia DATE NOT NULL,
            data_mes_referencia DATE NOT NULL,
            valor NUMERIC(10,2) NOT NULL,
            nis_beneficiario VARCHAR(50) REFERENCES beneficiario(nis),
            codigo_ibge_municipio VARCHAR(20) REFERENCES municipio(codigo_ibge),
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        )
        """
    )
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                for i, command in enumerate(commands, 1):
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        print(f"[Erro] Falha ao executar comando {i}: {e}")
                        raise
            conn.commit()
            print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"[Erro crítico] Não foi possível criar as tabelas: {e}")

def insert_data_on_db(df_municipio, df_beneficiario, df_saque):
    try:
        print("\nInserindo dados no DB\n")
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                #INSERT municípios
                for _, row in df_municipio.iterrows():
                    cur.execute("""
                        INSERT INTO municipio 
                        (codigo_ibge, nome, codigo_regiao, nome_regiao, uf_sigla, uf_nome)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (codigo_ibge) DO NOTHING
                    """, tuple(row))

                #INSERT beneficiários
                for _, row in df_beneficiario.iterrows():
                    cur.execute("""
                        INSERT INTO beneficiario 
                        (nis, cpf, nome, cpf_formatado)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (nis) DO NOTHING
                    """, tuple(row))

                #INSERT saques
                for _, row in df_saque.iterrows():
                    cur.execute("""
                        INSERT INTO saque 
                        (id_original, data_mes_competencia, data_mes_referencia, valor, nis_beneficiario, codigo_ibge_municipio)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, tuple(row))

                conn.commit()
                print("Dados inseridos no banco com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados no banco; {e}")

def truncate_db():
    
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                #COnsulta todas as tabelas publicas
                cur.execute("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public';
                """)
                tables = cur.fetchall()

                #Gerando a query dinamicamente - TRUNCATE com CASCADE
                if tables:
                    table_names = [f'"public"."{t[0]}"' for t in tables]
                    truncate_query = f'TRUNCATE TABLE {", ".join(table_names)} CASCADE;'
                    cur.execute(truncate_query)
                    print("Todas as tabelas foram zeradas com sucesso.")
                else:
                    print("Nenhuma tabela encontrada para truncar.")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Erro ao truncar as tabelas: {e}")

if __name__ == "__main__":
    test_db_conn()
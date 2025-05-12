import pandas as pd
import matplotlib.pyplot as plt
from config import DB_CONFIG

def gerar_visualizacoes():
    """Gera gráficos simples a partir do banco"""
    engine = create_engine(
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )
    
    # Gráfico 1: Top 10 órgãos
    query = """
    SELECT nome_orgao, SUM(valor) as total 
    FROM despesas 
    GROUP BY nome_orgao 
    ORDER BY total DESC 
    LIMIT 10
    """
    top_orgaos = pd.read_sql(query, engine)
    
    plt.figure(figsize=(10, 6))
    plt.barh(top_orgaos['nome_orgao'], top_orgaos['total'])
    plt.title('Top 10 Órgãos por Despesa')
    plt.tight_layout()
    plt.savefig('visualizacoes/top_orgaos.png')
    plt.close()
    
    print("Visualizações geradas em: visualizacoes/")
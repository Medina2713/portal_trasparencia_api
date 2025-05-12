import pandas as pd
import os
import json

def process_data():
    
    dados_combinados = []
    
    for arquivo in os.listdir("data/raw"):
        if arquivo.endswith(".json"):
            with open(f"data/raw/{arquivo}") as f:
                dados_combinados.extend(json.load(f))
    
    # Converte para DataFrame e faz limpeza básica
    df = pd.DataFrame(dados_combinados)
    print(f"Data frame {df.columns}")
    df['valorSaque'] = pd.to_numeric(df['valorSaque'], errors='coerce')
    #df = df.dropna(subset=['valor'])
    
    # Salva os dados processados
    
    print(f"Dados processados salvos. Total: {len(df)} registros")
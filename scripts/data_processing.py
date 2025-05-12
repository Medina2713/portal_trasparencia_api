import pandas as pd
import os
import json

#mostra todas as colunas ao printar na tela
pd.set_option('display.max_columns',100)
    
def process_data():
    dados_combinados = []

    for arquivo in os.listdir("data/raw"):
        if arquivo.endswith(".json"):
            with open(f"data/raw/{arquivo}") as f:
                dados_combinados.extend(json.load(f))

    #Cria DataFrame geral
    df = pd.DataFrame(dados_combinados)
    df['valorSaque'] = pd.to_numeric(df['valorSaque'], errors='coerce')

    #Cria DF municipio
    df_municipio = pd.json_normalize(df['municipio'])
    df_municipio = df_municipio[[
        'codigoIBGE', 'nomeIBGE', 'codigoRegiao',
        'nomeRegiao', 'uf.sigla', 'uf.nome'
    ]].drop_duplicates()
    df_municipio.columns = [
        'codigo_ibge', 'nome', 'codigo_regiao',
        'nome_regiao', 'uf_sigla', 'uf_nome'
    ]

    #Cria DF dos benificiarios
    df_beneficiario = pd.json_normalize(df['beneficiarioNovoBolsaFamilia'])
    df_beneficiario = df_beneficiario[['nis', 'cpfFormatado', 'nome']]
    df_beneficiario.columns = ['nis', 'cpf_formatado', 'nome']
    df_beneficiario['cpf'] = df_beneficiario['cpf_formatado'].str.replace(r'\D', '', regex=True)

    #Cria DF dos saques
    df_saque = df[['id', 'dataMesCompetencia', 'dataMesReferencia', 'valorSaque']].copy()
    df_saque['nis_beneficiario'] = df_beneficiario['nis']
    df_saque['codigo_ibge_municipio'] = pd.json_normalize(df['municipio'])['codigoIBGE']
    df_saque.columns = [
        'id_original', 'data_mes_competencia',
        'data_mes_referencia', 'valor', 'nis_beneficiario', 'codigo_ibge_municipio'
    ]
   
    print(f"Dados processados. Registros: {len(df)}")
    return df_municipio, df_beneficiario, df_saque

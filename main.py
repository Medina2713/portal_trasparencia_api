'''import sys
print(sys.path)  # Verifica os caminhos de importação
from config import API_KEY
print(API_KEY)  # Testa se a importação funciona'''

import argparse
from scripts.database import *
from scripts.data_collection import *
from scripts.data_processing import process_data
#from scripts.database import carregar_banco
#from scripts.visualization import gerar_visualizacoes

def main():
   ''' parser = argparse.ArgumentParser(description="Processo de dados do Portal da Transparência")
    
    parser.add_argument('--coletar', action='store_true', help='Coletar dados da API')
    parser.add_argument('--processar', action='store_true', help='Processar dados coletados')
    parser.add_argument('--banco', action='store_true', help='Carregar dados no banco')
    parser.add_argument('--visualizar', action='store_true', help='Gerar visualizações')
    parser.add_argument('--tudo', action='store_true', help='Executar todo o pipeline')
    
    args = parser.parse_args()

    if args.coletar or args.tudo:
        print("Coletando dados da API...")
        get_bf_withdrawals_by_city_api('2024','01','4106902')
    
    if args.processar or args.tudo:
        print("\nProcessando dados...")
        process_data()
    
    if args.banco or args.tudo:
        print("\nCarregando no banco de dados...")
        carregar_banco()
    
    if args.visualizar or args.tudo:
        print("\nGerando visualizações...")
        gerar_visualizacoes()  '''
        
#get_data_api(2023)
#get_bf_withdrawals_by_city_api('2024','01','4106902')
test_db_conn()


if __name__ == "__main__":
    main()
import argparse
from scripts.database import *
from scripts.data_collection import *
from scripts.data_processing import *
from scripts.temp_files import *

def main():
    parser = argparse.ArgumentParser(description="Pipeline de dados do Bolsa Família")
    
    parser.add_argument('--coletar', action='store_true', help='Coletar dados da API')
    parser.add_argument('--processar', action='store_true', help='Processar dados coletados')
    parser.add_argument('--banco', action='store_true', help='Carregar dados no banco')
    parser.add_argument('--limpar', action='store_true', help='Limpar dados temporários')
    parser.add_argument('--tudo', action='store_true', help='Executar todo o pipeline')
    
    args = parser.parse_args()

    if args.limpar:
        print("Truncando o DB\n")
        truncate_db()
        clear_temp_data()
        print("Dados temporários removidos!")
        return

    if args.coletar or args.tudo:
        print("Coletando dados...")
        get_bf_withdrawals_by_city_api(YEAR_RQST, MONTH_RQST, CITY_CODE)

    if args.processar or args.tudo:
        print("\nProcessando dados...")
        dfs = process_data()  
        save_temp_data(*dfs)
        print("Dados salvos temporariamente")

    if args.banco or args.tudo:
        print(f"Criando as tabelas")
        print("\nCarregando no banco...")
        create_tables()
        
        
        if not temp_data_exists() and not args.tudo:
            print("Execute --processar primeiro")
            return
            
        dfs = load_temp_data()
        if all(df is not None for df in dfs):
            insert_data_on_db(*dfs)
            if not args.tudo:
                clear_temp_data()
        else:
            print("Dados corrompidos. Reprocesse os dados")

if __name__ == "__main__":
    main()
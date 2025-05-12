import requests
import time
import json
import glob
from config import *


def get_bf_withdrawals_by_city_api(year, month, city_code):
    
    raw_folder = "data/raw"
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder)
    else:
        files = glob.glob(os.path.join(raw_folder, "*.json"))
        for file in files:
            os.remove(file)
        print(f"[INFO] Pasta '{raw_folder}' limpa antes da coleta dos dados.")
    
    endpoint = "novo-bolsa-familia-sacado-beneficiario-por-municipio"
    headers = {"chave-api-dados": API_KEY,
               "accept": "*/*"}
    
    for month in range(int(month), 13):  # Apenas 2 meses para exemplo
        mesAno = f"{year}{month:02d}"
        pagina = 1
        while True:
            if pagina > PAGES_LIMIT:
                print(f"Atingimos o limite de páginas")
                break
            
            try:
                url = f"{API_BASE_URL}{endpoint}?mesAno={mesAno}&codigoIbge={city_code}&pagina={pagina}"
                print(f"URL da REQUEST: {url}")
                response = requests.get(
                    url,
                    headers=headers
                    
                )
                #response.raise_for_status()
                
                dados = response.json()
                if not dados:
                    break
                
                # Salva cada página como um arquivo separado
                with open(f"data/raw/Saques_BF_{year}_{month}_{pagina}.json", "w") as f:
                    json.dump(dados, f)
                
                print(f"Coletados {len(dados)} registros de {month}/{year} (pág {pagina})")
                pagina += 1
                time.sleep(API_RATE_LIMIT)
                
            except Exception as e:
                print(f"Erro ao coletar dados: {e}")
                break
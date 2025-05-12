import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


# Configurações da API
API_BASE_URL = os.getenv('API_BASE_URL')
API_KEY = os.getenv('API_KEY')
API_RATE_LIMIT = float(os.getenv('API_RATE_LIMIT', 1))
API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
PAGES_LIMIT = 3
CITY_CODE ='4106902'
YEAR_RQST ='2024'
MONTH_RQST ='01'

# Configurações do Banco

DB_HOST= os.getenv('DB_HOST'),
DB_PORT= os.getenv('DB_PORT'),
DB_NAME= os.getenv('DB_NAME'),
DB_USER= os.getenv('DB_USER'),
DB_PASSWORD= os.getenv('DB_PASS')



    
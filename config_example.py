
API_CONFIG = {
    'BASE_URL': 'https://api.portaldatransparencia.gov.br/api-de-dados/',
    'API_KEY': '0000000000000000000000000000',  
    'RATE_LIMIT': 1,  
    'MAX_RETRIES': 3  
}


DB_LOCAL = {
    'host': 'localhost',
    'database': 'portal_transparencia',
    'user': 'postgres',
    'password': 'sua_senha',
    'port': '5432'
}


DB_GOOGLE_CLOUD = {
    'host': 'seu_ip_publico',  # IP da instância
    'database': 'portal_transparencia',
    'user': 'postgres',  # ou usuário específico
    'password': 'sua_senha_cloud',
    'port': '5432'
}



# Configurações das visualizações
VIZ_CONFIG = {
    'PLOT_STYLE': 'seaborn',  # estilo dos gráficos
    'COLOR_PALETTE': 'viridis',
    'WIDTH': 12,  # polegadas
    'HEIGHT': 6
}

# Configurações de diretórios
DIR_CONFIG = {
    'RAW_DATA': 'data/raw',
    'PROCESSED_DATA': 'data/processed',
    'VIZ_OUTPUT': 'visualizations'
}
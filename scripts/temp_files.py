from pathlib import Path
import pandas as pd
#import shutil

TEMP_DIR = Path("data/temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def save_temp_data(df_municipio, df_beneficiario, df_saque):
   
    df_municipio.to_parquet(TEMP_DIR / "municipio.parquet")
    df_beneficiario.to_parquet(TEMP_DIR / "beneficiario.parquet")
    df_saque.to_parquet(TEMP_DIR / "saque.parquet")

def load_temp_data():
    
    try:
        return (
            pd.read_parquet(TEMP_DIR / "municipio.parquet"),
            pd.read_parquet(TEMP_DIR / "beneficiario.parquet"),
            pd.read_parquet(TEMP_DIR / "saque.parquet")
        )
    except FileNotFoundError:
        return None, None, None

def clear_temp_data():
    
    for file in TEMP_DIR.glob("*.parquet"):
        file.unlink()

def temp_data_exists():
    
    return (TEMP_DIR / "municipio.parquet").exists()
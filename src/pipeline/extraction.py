import json
from pathlib import Path
from datetime import datetime

import requests
from src.logger import logger

from src.config import settings


def fetch_financial_api(url: str = settings.API_URL) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Requisição em {url} feita com sucesso!")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

def save_raw_data(data: dict, output_dir: str = "data/raw") -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True,  exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path=  path / f"raw_data_{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Arquivo salvo com sucesso em {file_path}!")
    return file_path

if __name__=="__main__":
    dados = fetch_financial_api()
    save_raw_data(dados)
import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_latest_raw_data(output_dir : str = "data/raw") -> Path:
    path = Path(output_dir)
    json_files = sorted(path.glob("raw_data*.json"))
    if not json_files:
        raise FileNotFoundError(f"Arquivo nao encontrado: {output_dir}")
    latest_raw_data = json_files[-1]
    logging.info(f"Arquivo encontrado! {latest_raw_data}")
    return latest_raw_data

def transform_data(file_path : Path) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data.values())
    df = df[["code", "name", "high", "low", "bid", "ask", "create_date"]]
    df = df.rename(
        columns={
            "code": "moeda",
            "name": "nome",
            "high": "maxima",
            "low": "minima",
            "bid": "compra",
            "ask": "venda",
            "create_date": "data_cotacao",
        }
    )
    colunas_numericas = ["maxima", "minima", "compra", "venda"]
    for coluna in colunas_numericas:
        df[coluna] = df[coluna].astype(float)
    logging.info("Dados transformados com sucesso!")
    return df

def save_processed_data(df : pd.DataFrame, output_dir: str = "data/processed") -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = path /f"processed_data_{timestamp}.csv"
    df.to_csv(file_path, index=False, encoding="utf-8")
    logging.info(f"Arquivo salvo em: {file_path}")
    return file_path

if __name__=="__main__":
    latest_raw_data = get_latest_raw_data()
    transformed_data = transform_data(latest_raw_data)
    saved_processed_data = save_processed_data(transformed_data)
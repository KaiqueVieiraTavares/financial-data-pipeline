import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_df(df: pd.DataFrame) -> bool:
    if df.empty:
        logging.error("DataFrame vazio!")
        return False
    colunas_obrigatorias = ["moeda", "nome", "maxima", "minima", "compra", "venda", "data_cotacao"]
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            logging.error(f"Falha na validacao! coluna: {coluna} ausente!")
            return False

    if df[colunas_obrigatorias].isnull().any().any():
        logging.error("Falha na validacao! Existem valores nulos nos dados")
        return False
    colunas_numericas = ["maxima", "minima", "compra", "venda"]
    for coluna in colunas_numericas:
        if (df[coluna] <=0).any():
            logging.error(f"Falha na validacao! Coluna: {coluna} possui valores menores ou iguais a zero!")
            return False

    logging.info("Dados validados com sucesso!")
    return True



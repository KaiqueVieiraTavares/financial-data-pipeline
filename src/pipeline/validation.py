import pandas as pd


from src.logger import logger

def validate_df(df: pd.DataFrame) -> bool:
    if df.empty:
        logger.error("DataFrame vazio!")
        return False
    colunas_obrigatorias = ["moeda", "nome", "maxima", "minima", "compra", "venda", "data_cotacao"]
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            logger.error(f"Falha na validacao! coluna: {coluna} ausente!")
            return False

    if df[colunas_obrigatorias].isnull().any().any():
        logger.error("Falha na validacao! Existem valores nulos nos dados")
        return False
    colunas_numericas = ["maxima", "minima", "compra", "venda"]
    for coluna in colunas_numericas:
        if (df[coluna] <=0).any():
            logger.error(f"Falha na validacao! Coluna: {coluna} possui valores menores ou iguais a zero!")
            return False

    logger.info("Dados validados com sucesso!")
    return True



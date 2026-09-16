import pandas as pd
from sqlalchemy import create_engine

from src.config import settings
from src.logger import logger


def load_data_to_postgres(
    df: pd.DataFrame,
    table_name: str = "cotacoes_moedas"
) -> None:
    try:
        engine = create_engine(settings.database_url)

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        logger.info(
            f"Dados inseridos com sucesso na tabela '{table_name}' no PostgreSQL!"
        )

    except Exception as e:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {e}")
        raise
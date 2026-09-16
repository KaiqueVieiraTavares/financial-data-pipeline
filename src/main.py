from pipeline.extraction import fetch_financial_api, save_raw_data
from pipeline.transformation import transform_data, save_processed_data
from pipeline.validation import validate_df
from pipeline.load import load_data_to_postgres
from logger import logger


def run_pipeline():
    logger.info("Iniciando a Pipeline de Dados Financeiros")

    #Extração
    raw_json = fetch_financial_api()
    raw_file_path = save_raw_data(raw_json)

    #Transformação
    df_transformed = transform_data(raw_file_path)

    #Validação
    if not validate_df(df_transformed):
        logger.error("Pipeline interrompida: Os dados não passaram no teste de validação!")
        raise ValueError("Dados inválidos. O processo foi abortado.")

    #Salvamento Dados Tratados
    processed_file_path = save_processed_data(df_transformed)

    #Envia DataFrame direto para o PostgreSQL no Docker 👈
    load_data_to_postgres(df_transformed, table_name="cotacoes_moedas")
    logger.info(f"Pipeline finalizada com sucesso! Arquivo gerado: {processed_file_path}")


if __name__ == "__main__":
    run_pipeline()
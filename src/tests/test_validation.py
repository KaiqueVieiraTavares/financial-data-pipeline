import pytest
import pandas as pd

from src.pipeline.validation import validate_df

@pytest.fixture()
def df_valido():
    return pd.DataFrame({
        "moeda": ["USD", "EUR"],
        "nome": ["Dólar Americano", "Euro"],
        "maxima": [5.25, 5.70],
        "minima": [5.15, 5.60],
        "compra": [5.20, 5.65],
        "venda": [5.21, 5.66],
        "data_cotacao": ["2026-09-16 10:00:00", "2026-09-16 10:00:00"]
    })


def test_validate_df_valido(df_valido: pd.DataFrame) -> None:
    result = validate_df(df_valido)
    assert result is True

def test_validate_df_vazio() -> None:
    df_vazio = pd.DataFrame()
    result = validate_df(df_vazio)
    assert result is False

def test_validate_df_coluna_ausente(df_valido: pd.DataFrame) -> None:
    df_valido = df_valido.drop(columns=["maxima"])
    result = validate_df(df_valido)
    assert result is False

def test_validate_df_numeros_menores_ou_iguais_zero(df_valido: pd.DataFrame) -> None:
    df_valido.loc[0, "maxima"] = 0
    result = validate_df(df_valido)
    assert result is False

def test_validate_df_valores_nulos(df_valido: pd.DataFrame) -> None:
    df_valido.loc[0, "nome"] = None
    result = validate_df(df_valido)
    assert result is False

def test_validate_df_valor_nao_numerico(df_valido: pd.DataFrame) -> None:
    df_valido.loc[0, "minima"] = "teste"
    result = validate_df(df_valido)
    assert result is False
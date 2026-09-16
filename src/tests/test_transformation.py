import pytest
import json
import pandas as pd
from pathlib import Path
from src.pipeline.transformation import get_latest_raw_data, transform_data, save_processed_data



@pytest.fixture()
def sample_json_data():
    return {
        "USDBRL": {
            "code": "USD",
            "name": "Dólar Americano/Real Brasileiro",
            "high": "5.2500",
            "low": "5.1500",
            "bid": "5.2000",
            "ask": "5.2010",
            "create_date": "2023-10-25 10:30:00"
        }
    }


def test_get_latest_raw_data_success(tmp_path: Path) -> None:
    (tmp_path / "raw_data_20231023.json").touch()
    (tmp_path / "raw_data_20231025.json").touch()
    (tmp_path / "raw_data_20231024.json").touch()

    latest_path = get_latest_raw_data(output_dir=str(tmp_path))

    assert latest_path.name ==  "raw_data_20231025.json"

def test_get_latest_raw_data_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Arquivo nao encontrado"):
        get_latest_raw_data(output_dir=str(tmp_path))


def test_transform_data(tmp_path: Path, sample_json_data: dict) -> None:
    file_path = tmp_path/"raw_data_test.json"
    with open (file_path, "w", encoding="utf-8") as f:
        json.dump(sample_json_data, f, indent=4)

    df = transform_data(file_path)


    assert isinstance(df, pd.DataFrame)
    colunas_obrigatorias = ["moeda", "nome", "maxima", "minima", "compra", "venda", "data_cotacao"]
    assert list(df.columns) == colunas_obrigatorias
    assert pd.api.types.is_datetime64_any_dtype(df["data_cotacao"])
    assert all(
        pd.api.types.is_float_dtype(df[col])
        for col in ["maxima", "minima", "compra", "venda"]
    )
    assert df["maxima"].iloc[0] == 5.2500


def test_save_processed_data(tmp_path: Path) -> None:
    df = pd.DataFrame({
        "moeda": ["USD"],
        "compra": [5.20]
    })

    saved_file_path = save_processed_data(df, output_dir=str(tmp_path))

    assert saved_file_path.exists()
    assert saved_file_path.suffix == ".csv"

    saved_df = pd.read_csv(saved_file_path)
    assert saved_df["compra"].iloc[0] == 5.20
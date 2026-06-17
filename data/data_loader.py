from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


NUMERIC_COLUMNS: List[str] = [
    "FACTURACION_PROMEDIO",
    "M3_PROMEDIO",
    "VALOR_PAGO_PROMEDIO",
    "FACTURACION_PERIODO",
    "M3_PERIODO",
    "CANTIDAD_AJUSTES_ULT_6_MESES",
    "VALOR_AJUSTE_PROMEDIO",
    "VALOR_AJUSTE_PERIODO",
]


REQUIRED_COLUMNS: List[str] = [
    "CUENTA",
    "ACD_CODIGO",
    "CICLO",
    "CATEGORIA",
    "PLAN_FACTURACION",
    "FACTURACION_PROMEDIO",
    "M3_PROMEDIO",
    "VALOR_PAGO_PROMEDIO",
    "FACTURACION_PERIODO",
    "M3_PERIODO",
    "CANTIDAD_AJUSTES_ULT_6_MESES",
    "VALOR_AJUSTE_PROMEDIO",
    "VALOR_AJUSTE_PERIODO",
]


def validate_columns(df: pd.DataFrame) -> None:
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Columnas faltantes: {sorted(missing)}"
        )


def clean_numeric_column(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(",", ".", regex=False)
        .replace(
            ["nan", "None", ""],
            np.nan
        )
        .astype(float)
    )


def create_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df["DELTA_M3"] = (
        df["M3_PERIODO"]
        - df["M3_PROMEDIO"]
    )

    df["DELTA_FACTURACION"] = (
        df["FACTURACION_PERIODO"]
        - df["FACTURACION_PROMEDIO"]
    )

    df["PORCENTAJE_VARIACION_M3"] = (
        df["DELTA_M3"]
        /
        df["M3_PROMEDIO"].replace(0, np.nan)
    ) * 100

    df["PORCENTAJE_VARIACION_FACTURACION"] = (
        df["DELTA_FACTURACION"]
        /
        df["FACTURACION_PROMEDIO"].replace(0, np.nan)
    ) * 100

    # Variable objetivo futura

    df["TARGET_AJUSTE"] = (
        df["VALOR_AJUSTE_PERIODO"]
        .fillna(0)
        .ne(0)
        .astype(int)
    )

    return df


def load_dataset(
    path: Path
) -> pd.DataFrame:

    df = pd.read_csv(
        path,
        sep=";",
        encoding="latin-1"
    )

    validate_columns(df)

    for column in NUMERIC_COLUMNS:
        df[column] = clean_numeric_column(
            df[column]
        )

    df = df.fillna(0)

    df = create_features(df)

    return df
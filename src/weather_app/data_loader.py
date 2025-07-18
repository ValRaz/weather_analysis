import pandas as pd
from pathlib import Path

# Sets up base folders
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Reads the global monthly anomalies CSV, cleans once, caches, and loads the cleaned file
def load_monthly_anomalies(
    raw_file: str = "Global Land and Ocean Average Temperature Anomalies.csv",
    date_col: str = "Date",
    anomaly_col: str = "Anomaly",
    cache_file: str = "global_temp_anomalies_1980_2024.csv"
) -> pd.DataFrame:
    cache_path = PROCESSED_DIR / cache_file
    raw_path   = RAW_DIR / raw_file

    if not cache_path.exists():
        df = pd.read_csv(raw_path, comment="#")
        df = df.dropna(subset=[date_col, anomaly_col])
        df[date_col] = df[date_col].astype(str)
        df["Year"]  = df[date_col].str[:4].astype(int)
        df["Month"] = df[date_col].str[4:6].astype(int)
        df = df[(df["Year"] >= 1980) & (df["Year"] <= 2024)]
        df.to_csv(cache_path, index=False)

    return pd.read_csv(cache_path)


# Reads the billion-dollar disasters CSV, cleans once, caches, and loads the cleaned file
def load_disasters(
    raw_file: str = "Billion-Dollar Disasters from 1980-2023.csv",
    begin_col: str = "Begin Date",
    cache_file: str = "disasters_1980_2023.csv"
) -> pd.DataFrame:
    cache_path = PROCESSED_DIR / cache_file
    raw_path   = RAW_DIR / raw_file

    if not cache_path.exists():
        df = pd.read_csv(raw_path, skiprows=2)
        df = df.dropna(subset=[begin_col])
        df[begin_col] = pd.to_datetime(
            df[begin_col].astype(str),
            format="%Y%m%d",
            errors="coerce"
        )
        df = df.dropna(subset=[begin_col])
        df["Year"] = df[begin_col].dt.year
        df = df[(df["Year"] >= 1980) & (df["Year"] <= 2023)]
        df.to_csv(cache_path, index=False)

    return pd.read_csv(cache_path, parse_dates=[begin_col])
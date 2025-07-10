import pandas as pd
from pathlib import Path

# Sets up base folders
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Checks for processed folder
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Reads all 1980-2024 CSVs, cleans once, caches, and loads the cleaned file
def load_monthly_normals(
    raw_pattern: str = "*-1980-2024-normals-daily-*.csv",
    date_col: str = "DATE",
    temp_col: str = "DLY-TAVG-NORMAL",
    cache_file: str = "monthly_normals_1980_2024.csv"
) -> pd.DataFrame:
    cache_path = PROCESSED_DIR / cache_file
    if not cache_path.exists():
        files = sorted(RAW_DIR.glob(raw_pattern))
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
        df[date_col] = pd.to_datetime(df[date_col], format="%m-%d", errors="coerce")
        df = df.dropna(subset=[date_col, temp_col])
        df.to_csv(cache_path, index=False)
    return pd.read_csv(cache_path, parse_dates=[date_col])


# Reads all 1991-2020 baseline CSVs, cleans once, caches, and loads the cleaned file
def load_baseline_normals(
    raw_pattern: str = "*-normals-daily-1991-2020-*.csv",
    date_col: str = "DATE",
    temp_col: str = "DLY-TAVG-NORMAL",
    cache_file: str = "baseline_normals_1991_2020.csv"
) -> pd.DataFrame:
    cache_path = PROCESSED_DIR / cache_file
    if not cache_path.exists():
        files = sorted(RAW_DIR.glob(raw_pattern))
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
        df[date_col] = pd.to_datetime(df[date_col], format="%m-%d", errors="coerce")
        df[temp_col] = df[temp_col].ffill().bfill()
        df = df.dropna(subset=[date_col])
        df.to_csv(cache_path, index=False)
    return pd.read_csv(cache_path, parse_dates=[date_col])


# Reads billion-dollar disaster frequency CSV, cleans once, caches, and loads the cleaned file
def load_disasters(
    raw_file: str = "billion-dollar-disaster-frequency-data.csv",
    year_col: str = "year",
    cache_file: str = "billion_dollar_disasters_1980_2024.csv"
) -> pd.DataFrame:
    cache_path = PROCESSED_DIR / cache_file
    if not cache_path.exists():
        csv_path = RAW_DIR / raw_file
        if not csv_path.exists():
            raise FileNotFoundError(f"Disaster CSV not found at {csv_path}")
        df = pd.read_csv(csv_path)
        df = pd.read_csv(csv_path, skiprows=1)
        df[year_col] = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
        df = df.dropna(subset=[year_col])
        df = df.rename(columns={year_col: "Year"})
        df = df[(df["Year"] >= 1980) & (df["Year"] <= 2024)]
        df.to_csv(cache_path, index=False)
    return pd.read_csv(cache_path)
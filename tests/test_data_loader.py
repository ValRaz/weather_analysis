import pandas as pd
import pytest
from weather_app.data_loader import (
    load_monthly_anomalies,
    load_disasters
)

# Loads the cleaned global temperature anomalies (1980–2024)
@pytest.fixture(scope="module")
def anomalies_df():
    return load_monthly_anomalies()

# Loads the cleaned disaster events (1980–2023)
@pytest.fixture(scope="module")
def disasters_df():
    return load_disasters()

# Tests function to load global temperature anomalies
def test_load_monthly_anomalies_shape_and_types(anomalies_df):
    assert isinstance(anomalies_df, pd.DataFrame)
    for col in ("Date", "Year", "Month", "Anomaly"):
        assert col in anomalies_df.columns, f"Missing column {col}"
    assert pd.api.types.is_integer_dtype(anomalies_df["Year"])
    assert pd.api.types.is_integer_dtype(anomalies_df["Month"])
    assert anomalies_df["Anomaly"].dtype.kind in ("i", "u", "f")
    assert anomalies_df["Anomaly"].notna().all()
    years = anomalies_df["Year"].unique()
    assert years.min() >= 1980 and years.max() <= 2024

# Tests function to load billion-dollar disaster frequency data
def test_load_disasters_year_range_and_columns(disasters_df):
    assert isinstance(disasters_df, pd.DataFrame)
    for col in ("Begin Date", "Year"):
        assert col in disasters_df.columns, f"Missing column {col}"
    assert pd.api.types.is_datetime64_any_dtype(disasters_df["Begin Date"])
    assert disasters_df["Begin Date"].notna().all()
    assert pd.api.types.is_integer_dtype(disasters_df["Year"])
    yrs = disasters_df["Year"].unique()
    assert yrs.min() >= 1980 and yrs.max() <= 2023
    assert len(disasters_df) > 0
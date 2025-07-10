import pandas as pd
import pytest
from weather_app.data_loader import (
    load_monthly_normals,
    load_baseline_normals,
    load_disasters
)

@pytest.fixture(scope="module")
def normals_df():
    return load_monthly_normals()

@pytest.fixture(scope="module")
def baseline_df():
    return load_baseline_normals()

@pytest.fixture(scope="module")
def disasters_df():
    return load_disasters()

# Tests function to load monthly normals 1980-2024 data
def test_load_monthly_normals_shape_and_types(normals_df):
    assert isinstance(normals_df, pd.DataFrame)
    assert "DATE" in normals_df.columns
    assert "DLY-TAVG-NORMAL" in normals_df.columns
    assert normals_df["DATE"].notna().all()
    assert normals_df["DLY-TAVG-NORMAL"].notna().all()

# Tests function to load monthly normals 1991-2020 data
def test_load_baseline_normals_complete_coverage(baseline_df):
    assert isinstance(baseline_df, pd.DataFrame)
    assert baseline_df["DATE"].notna().all()
    assert baseline_df["DLY-TAVG-NORMAL"].notna().all()
    assert baseline_df["DLY-TAVG-NORMAL"].isna().sum() == 0

# Tests function to load billion dollar disaster frequency data
def test_load_disasters_year_range_and_columns(disasters_df):
    assert isinstance(disasters_df, pd.DataFrame)
    assert "Year" in disasters_df.columns
    years = disasters_df["Year"].unique()
    assert years.min() >= 1980
    assert years.max() <= 2024
    assert "state" in disasters_df.columns
    assert len(disasters_df) > 0
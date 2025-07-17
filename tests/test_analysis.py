import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from math import isnan

from weather_app.analysis import (
    compute_annual_anomalies,
    compute_annual_disasters,
    compute_baseline_offset
)

@pytest.fixture
def sample_anomalies():
    # One out-of-range year (1979), two in 1980, one in 1981, one missing (1982)
    return pd.DataFrame({
        "Year":    [1979, 1980, 1980, 1981, 1982],
        "Anomaly": [0.5,  0.2,  0.4,  -0.1,   None]
    })

# Tests compute_annual_anomalies over a valid range
def test_compute_annual_anomalies_basic(sample_anomalies):
    result = compute_annual_anomalies(sample_anomalies, start_year=1980, end_year=1981)

    expected = pd.DataFrame({
        "Year":             [1980,  1981],
        "Annual_Anomaly_C": [0.3,   -0.1]
    })

    assert_frame_equal(
        result.reset_index(drop=True),
        expected.reset_index(drop=True),
        check_dtype=False,
        atol=1e-8
    )

# Tests that out-of-range requests yield an empty DataFrame with correct columns
def test_compute_annual_anomalies_out_of_range(sample_anomalies):
    result = compute_annual_anomalies(sample_anomalies, start_year=1990, end_year=2000)
    assert result.empty
    assert list(result.columns) == ["Year", "Annual_Anomaly_C"]

# Tests compute_baseline_offset over a simple annual_anomalies DataFrame
def test_compute_baseline_offset_basic():
    # Create a toy annual anomalies DF
    toy = pd.DataFrame({
        "Year":             [1980, 1981, 1982, 1983],
        "Annual_Anomaly_C": [ 0.0,  0.2,   0.4,   0.6]
    })

    # Baseline from 1981 to 1983 → mean(0.2,0.4,0.6) = 0.4
    offset = compute_baseline_offset(toy, baseline_start=1981, baseline_end=1983)
    assert pytest.approx(offset, rel=1e-6) == 0.4

# Tests compute_baseline_offset when no years fall in the baseline window
def test_compute_baseline_offset_empty():
    toy = pd.DataFrame({
        "Year":             [2000, 2001],
        "Annual_Anomaly_C": [ 1.0,  1.2]
    })

    # Baseline window 1980-1990 contains no rows → mean should be NaN
    offset = compute_baseline_offset(toy, baseline_start=1980, baseline_end=1990)
    assert isnan(offset)

@pytest.fixture
def sample_disasters():
    # One out-of-range year (1979), two in 1980, three in 1981
    return pd.DataFrame({
        "Year": [1979, 1980, 1980, 1981, 1981, 1981]
    })

# Tests compute_annual_disasters over a valid range
def test_compute_annual_disasters_basic(sample_disasters):
    result = compute_annual_disasters(sample_disasters, start_year=1980, end_year=1981)

    expected = pd.DataFrame({
        "Year":          [1980, 1981],
        "Disaster_Count":[2,    3]
    })

    assert_frame_equal(
        result.reset_index(drop=True),
        expected.reset_index(drop=True),
        check_dtype=False
    )

# Tests that requesting an out-of-range disaster count returns an empty DataFrame
def test_compute_annual_disasters_empty(sample_disasters):
    result = compute_annual_disasters(sample_disasters, start_year=1990, end_year=2000)
    assert result.empty
    assert list(result.columns) == ["Year", "Disaster_Count"]
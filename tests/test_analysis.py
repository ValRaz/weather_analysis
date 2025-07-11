import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_app.analysis import (
    compute_annual_anomalies,
    compute_annual_disasters
)

@pytest.fixture
def sample_anomalies():
    # Creates a small anomalies data frame containing one record out of range, two in 1980, one in 1981, and one missing value for 1982
    return pd.DataFrame({
        "Year":    [1979, 1980, 1980, 1981, 1982],
        "Anomaly": [0.5,  0.2,  0.4,  -0.1,   None]
    })

# Tests the function to compute mean annual anomalies.
def test_compute_annual_anomalies_basic(sample_anomalies):
    result = compute_annual_anomalies(sample_anomalies, start_year=1980, end_year=1981)

    expected = pd.DataFrame({
        "Year":               [1980,  1981],
        "Annual_Anomaly_C":   [0.3,  -0.1]
    })

    assert_frame_equal(result.reset_index(drop=True),
                       expected.reset_index(drop=True),
                       check_dtype=False,
                       atol=1e-8)

# Tests out of range handling for the compute mean annual anomalies function.
def test_compute_annual_anomalies_out_of_range(sample_anomalies):
    result = compute_annual_anomalies(sample_anomalies, start_year=1990, end_year=2000)
    assert result.empty
    assert list(result.columns) == ["Year", "Annual_Anomaly_C"]

# Creates a small disasters data frame containing one record out of range, two in 1980 and one in 1981
@pytest.fixture
def sample_disasters():
    return pd.DataFrame({
        "Year": [1979, 1980, 1980, 1981, 1981, 1981]
    })

# Tests the compute annual disasters by year function
def test_compute_annual_disasters_basic(sample_disasters):
    result = compute_annual_disasters(sample_disasters, start_year=1980, end_year=1981)

    expected = pd.DataFrame({
        "Year":          [1980, 1981],
        "Disaster_Count":[2,    3]
    })

    assert_frame_equal(result.reset_index(drop=True),
                       expected.reset_index(drop=True),
                       check_dtype=False)

# Tests empty year handling for the compute annual disasters by year function.
def test_compute_annual_disasters_empty(sample_disasters):
    result = compute_annual_disasters(sample_disasters, start_year=1990, end_year=2000)
    assert result.empty
    assert list(result.columns) == ["Year", "Disaster_Count"]
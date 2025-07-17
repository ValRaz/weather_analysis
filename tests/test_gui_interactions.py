import pytest
import pandas as pd
import matplotlib

# Sets up non‐interactive backend for testing
matplotlib.use("Agg")
from matplotlib.figure import Figure
from weather_app.analysis import make_summary
from weather_app.visualization import plot_temperature_trend, plot_annual_disasters

@pytest.fixture
def rebased_sample():
    # simple rebased anomalies from 2000 to 2002
    return pd.DataFrame({
        "Year":               [2000, 2001, 2002],
        "Annual_Anomaly_C":   [0.10, 0.20, 0.40]
    })

# 1) Test the pure summary helper in gui.py
def test_make_summary_full_range(rebased_sample):
    text = make_summary(rebased_sample, start_year=2000, end_year=2002)
    # average = (0.10+0.20+0.40)/3 = 0.2333…, delta = 0.40−0.10 = +0.30
    assert "From 2000 to 2002" in text
    assert "0.23°C" in text
    assert "+0.30°C" in text
    assert "(from +0.10°C to +0.40°C)" in text

def test_make_summary_single_year(rebased_sample):
    text = make_summary(rebased_sample, start_year=2001, end_year=2001)
    # avg = 0.20, delta = 0.00
    assert "From 2001 to 2001" in text
    assert "0.20°C" in text
    assert "+0.00°C" in text

def test_make_summary_no_data(rebased_sample):
    # years outside the DataFrame
    text = make_summary(rebased_sample, start_year=1990, end_year=1995)
    assert text == "No data available for the selected year range."

# 2) Test that plot_temperature_trend draws exactly two lines:
#    –  the data series + the horizontal baseline
def test_plot_temperature_trend_lines():
    fig = Figure()
    ax  = fig.add_subplot(111)
    # minimal two‐point DataFrame
    df = pd.DataFrame({"Year":[2000,2001], "Annual_Anomaly_C":[0.1,0.2]})
    plot_temperature_trend(ax, df)
    lines = ax.get_lines()
    assert len(lines) == 2
    # first line is our data
    xs, ys = lines[0].get_xdata(), lines[0].get_ydata()
    assert list(xs) == [2000, 2001]
    assert list(ys) == [0.1, 0.2]

# 3) Test that plot_annual_disasters draws exactly one line
def test_plot_annual_disasters_lines():
    fig = Figure()
    ax  = fig.add_subplot(111)
    df = pd.DataFrame({"Year":[1980,1981,1982], "Disaster_Count":[5,7,6]})
    plot_annual_disasters(ax, df)
    lines = ax.get_lines()
    assert len(lines) == 1
    xs, ys = lines[0].get_xdata(), lines[0].get_ydata()
    assert list(xs) == [1980, 1981, 1982]
    assert list(ys) == [5,7,6]
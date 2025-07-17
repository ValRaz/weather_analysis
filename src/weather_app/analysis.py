import pandas as pd

# Computes the annual mean of the monthly anomalies (filtered by year range)
def compute_annual_anomalies(
    anomalies_df: pd.DataFrame,
    start_year: int,
    end_year: int
) -> pd.DataFrame:
    df = anomalies_df.dropna(subset=["Year", "Anomaly"]).copy()
    df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
    annual = (
        df.groupby("Year")["Anomaly"]
          .mean()
          .reset_index(name="Annual_Anomaly_C")
          .sort_values("Year")
    )
    return annual

# Computes the mean anomaly over the baseline period (1980-2010)
def compute_baseline_offset(
    annual_anomalies_df: pd.DataFrame,
    baseline_start: int,
    baseline_end: int
) -> float:
    # filters to the baseline years and takes the mean anomaly
    mask = ((annual_anomalies_df["Year"] >= baseline_start) &
            (annual_anomalies_df["Year"] <= baseline_end))
    return float(annual_anomalies_df.loc[mask, "Annual_Anomaly_C"].mean())

# Computes the total annual count of disasters (filtered by year range)
def compute_annual_disasters(
    disasters_df: pd.DataFrame,
    start_year: int,
    end_year: int
) -> pd.DataFrame:
    df = disasters_df.dropna(subset=["Year"]).copy()
    df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
    counts = (
        df.groupby("Year")
          .size()
          .reset_index(name="Disaster_Count")
          .sort_values("Year")
    )
    return counts

# Helper to produce the summary text for Question 1 for gui testing
def make_summary(rebased_df, start_year: int, end_year: int) -> str:
    first = rebased_df.loc[rebased_df["Year"] == start_year, "Annual_Anomaly_C"]
    last  = rebased_df.loc[rebased_df["Year"] == end_year,   "Annual_Anomaly_C"]
    if not first.empty and not last.empty:
        first_val = first.iloc[0]
        last_val  = last.iloc[0]
        avg_val   = rebased_df["Annual_Anomaly_C"].mean()
        delta     = last_val - first_val
        return (
            f"From {start_year} to {end_year}, average anomaly was "
            f"{avg_val:.2f}°C, changing by {delta:+.2f}°C "
            f"(from {first_val:+.2f}°C to {last_val:+.2f}°C)."
        )
    else:
        return "No data available for the selected year range."
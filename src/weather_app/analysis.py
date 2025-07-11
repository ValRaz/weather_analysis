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
import pandas as pd

# Computes the annual mean of the monthly anomalies (1980–2024)
def compute_annual_anomalies(anomalies_df: pd.DataFrame) -> pd.DataFrame:
    df = anomalies_df.dropna(subset=["Year", "Anomaly"]).copy()
    annual = (
        df.groupby("Year")["Anomaly"]
          .mean()
          .reset_index(name="Annual_Anomaly_C")
          .sort_values("Year")
    )
    return annual


# Computes the total annual count of disasters (1980–2023)
def compute_annual_disasters(disasters_df: pd.DataFrame) -> pd.DataFrame:
    df = disasters_df.dropna(subset=["Year"]).copy()
    counts = (
        df.groupby("Year")
          .size()
          .reset_index(name="Disaster_Count")
          .sort_values("Year")
    )
    return counts
# Plots annual temperature anomalies on the given axes
def plot_temperature_trend(ax, annual_anomalies_df):
    ax.plot(
        annual_anomalies_df["Year"],
        annual_anomalies_df["Annual_Anomaly_C"],
        marker="o",
        label="Annual Temp Anomaly"
    )
    ax.axhline(0, color="gray", linestyle="--", label="Baseline (1980–2010)")
    ax.set_title("Global Annual Temperature Anomalies (°C)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Anomaly (°C)")
    ax.legend()


# Plots annual disaster counts on the given axes
def plot_annual_disasters(ax, annual_disasters_df):
    ax.plot(
        annual_disasters_df["Year"],
        annual_disasters_df["Disaster_Count"],
        marker="s",
        color="red",
        label="Annual Disaster Count"
    )

    # Set titles and labels
    ax.set_title("U.S. Billion-Dollar Weather Disasters Count")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.legend()
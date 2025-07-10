import pandas as pd
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from weather_app.data_loader import (
    load_monthly_normals,
    load_baseline_normals,
    load_disasters
)

# Sets window appearance
def launch_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Loads cleaned data
    normals_df = load_monthly_normals()
    baseline_df = load_baseline_normals()
    disasters_df = load_disasters()

    # Converts the DATE (MM-DD) into a datetime and computes day of year
    normals_df["Date_dd"] = pd.to_datetime(normals_df["DATE"], format="%m-%d", errors="coerce")
    normals_df["DayOfYear"] = normals_df["Date_dd"].dt.dayofyear
    baseline_df["Date_dd"] = pd.to_datetime(baseline_df["DATE"], format="%m-%d", errors="coerce")
    baseline_df["DayOfYear"] = baseline_df["Date_dd"].dt.dayofyear

    # Computes daily normals in °F (tenths °F → °F)
    daily_normals_f   = normals_df["DLY-TAVG-NORMAL"] / 10.0
    daily_baseline_f  = baseline_df["DLY-TAVG-NORMAL"] / 10.0

    # Computes annual disaster counts by summing all event columns
    event_cols = [c for c in disasters_df.columns if c not in ("Year", "state")]
    annual_disasters = (
        disasters_df
        .groupby("Year")[event_cols]
        .sum()
        .sum(axis=1)
    )

    # Creates main window
    app = ctk.CTk()
    app.title("Weather Analysis Prototype")
    app.geometry("800x700")

    # Creates and displays daily-climatology frame
    daily_frame = ctk.CTkFrame(master=app)
    daily_frame.pack(fill="both", expand=True, padx=10, pady=5)

    fig1 = Figure(figsize=(6, 3), dpi=100)
    ax1  = fig1.add_subplot(111)
    ax1.plot(
        normals_df["DayOfYear"],
        daily_normals_f,
        marker=".", linestyle="", alpha=0.6,
        label="1980–2024 Daily Normals"
    )
    ax1.plot(
        baseline_df["DayOfYear"],
        daily_baseline_f,
        linestyle="--", color="black",
        label="1991–2020 Daily Baseline"
    )
    ax1.set_title("Climatological Daily Average Temperature")
    ax1.set_xlabel("Day of Year")
    ax1.set_ylabel("Avg Temp (°F)")
    ax1.legend(loc="upper right")

    canvas1 = FigureCanvasTkAgg(fig1, master=daily_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    # Creates and displays annual disaster frequency frame
    disc_frame = ctk.CTkFrame(master=app)
    disc_frame.pack(fill="both", expand=True, padx=10, pady=5)

    fig2 = Figure(figsize=(6, 3), dpi=100)
    ax2  = fig2.add_subplot(111)
    ax2.plot(
        annual_disasters.index,
        annual_disasters.values,
        marker="s",
        color="red",
        label="Annual Disaster Count"
    )
    ax2.set_title("Annual Billion-Dollar Disaster Count")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper left")

    canvas2 = FigureCanvasTkAgg(fig2, master=disc_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    app.mainloop()
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from weather_app.data_loader import load_monthly_anomalies, load_disasters
from weather_app.analysis import compute_annual_anomalies, compute_annual_disasters
from weather_app.visualization import plot_temperature_trend, plot_annual_disasters

# Sets window appearance and drives the application
def launch_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Loads processed data
    anomalies_df   = load_monthly_anomalies()
    disasters_df   = load_disasters()

    # Computes annual aggregates
    annual_anom = compute_annual_anomalies(anomalies_df)
    annual_disaster= compute_annual_disasters(disasters_df)

    # Builds main window
    app = ctk.CTk()
    app.title("Weather Analysis Prototype")
    app.geometry("800x700")

    # Creates temperature trend frame
    temp_frame = ctk.CTkFrame(master=app)
    temp_frame.pack(fill="both", expand=True, padx=10, pady=5)

    fig1 = Figure(figsize=(6, 3), dpi=100)
    ax1  = fig1.add_subplot(111)
    plot_temperature_trend(ax1, annual_anom)

    canvas1 = FigureCanvasTkAgg(fig1, master=temp_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    # Creates disaster count frame
    disc_frame = ctk.CTkFrame(master=app)
    disc_frame.pack(fill="both", expand=True, padx=10, pady=5)

    fig2 = Figure(figsize=(6, 3), dpi=100)
    ax2  = fig2.add_subplot(111)
    plot_annual_disasters(ax2, annual_disaster)

    canvas2 = FigureCanvasTkAgg(fig2, master=disc_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    app.mainloop()
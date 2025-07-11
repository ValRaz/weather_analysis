import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from weather_app.data_loader    import load_monthly_anomalies, load_disasters
from weather_app.analysis       import (
    compute_annual_anomalies,
    compute_annual_disasters,
    compute_baseline_offset
)
from weather_app.visualization  import plot_temperature_trend, plot_annual_disasters

# Sets window appearance and drives the application
def launch_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Loads processed data
    anomalies_df = load_monthly_anomalies()
    disasters_df = load_disasters()

    # Prepares main window
    app = ctk.CTk()
    app.title("Weather Analysis Prototype")
    app.geometry("800x750")

    # Creates the controls for year-range filtering
    control_frame = ctk.CTkFrame(master=app)
    control_frame.pack(fill="x", padx=10, pady=5)

    years     = [str(y) for y in range(1980, 2025)]
    start_var = ctk.StringVar(value="1980")
    end_var   = ctk.StringVar(value="2024")

    ctk.CTkLabel(master=control_frame, text="Start Year:").pack(side="left", padx=(0,5))
    start_menu = ctk.CTkOptionMenu(
        master=control_frame,
        values=years,
        variable=start_var
        )
    start_menu.pack(side="left", padx=(0,10))

    ctk.CTkLabel(master=control_frame, text="End Year:").pack(side="left", padx=(0,5))
    end_menu   = ctk.CTkOptionMenu(
        master=control_frame,
        values=years,
        variable=end_var
        )
    end_menu.pack(side="left")

    # Creates the temperature trend frame
    temp_frame = ctk.CTkFrame(master=app)
    temp_frame.pack(fill="both", expand=True, padx=10, pady=5)
    fig1 = Figure(figsize=(6, 3), dpi=100)
    ax1  = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=temp_frame)
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    # Creates the disaster count frame
    disc_frame = ctk.CTkFrame(master=app)
    disc_frame.pack(fill="both", expand=True, padx=10, pady=5)
    fig2 = Figure(figsize=(6, 3), dpi=100)
    ax2  = fig2.add_subplot(111)
    canvas2 = FigureCanvasTkAgg(fig2, master=disc_frame)
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    # Updates both plots when year-range changes
    def update_plots(_=None):
        start = int(start_var.get())
        end   = int(end_var.get())

        annual_anom     = compute_annual_anomalies(anomalies_df, start, end)
        annual_disaster = compute_annual_disasters(disasters_df, start, end)

        baseline_offset = compute_baseline_offset(annual_anom, 1981, 2010)

        rebased = annual_anom.copy()
        rebased["Annual_Anomaly_C"] = rebased["Annual_Anomaly_C"] - baseline_offset

        ax1.clear()
        plot_temperature_trend(ax1, rebased)
        canvas1.draw()

        ax2.clear()
        plot_annual_disasters(ax2, annual_disaster)
        canvas2.draw()

    # Binds dropdowns to trigger plot updates
    start_menu.configure(command=update_plots)
    end_menu.configure(command=update_plots)

    # Initial draw
    update_plots()

    app.mainloop()
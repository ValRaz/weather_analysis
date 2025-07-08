import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def launch_app():
    # Sets window appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Displays the main window
    app = ctk.CTk()
    app.title("Weather Analysis Prototype")
    app.geometry("600x400")

    # Creates a frame for the plot
    plot_frame = ctk.CTkFrame(master=app)
    plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Displays a sample Matplotlib figure
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    years = [2000, 2005, 2010, 2015, 2020]
    temps = [14.5, 14.7, 14.9, 15.1, 15.3]
    ax.plot(years, temps, marker="o")
    ax.set_title("Sample Temp Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg Temp (°C)")

    # Embeds the plot into CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    app.mainloop()
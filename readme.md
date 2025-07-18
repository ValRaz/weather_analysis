# Overview

This project explores long-ter climate trends by analyzing two freely available datasets. The following are the datasets I used from github datasets (from datahub.io), and NOAA:
* [CPI Adjusted United States Billion Dollar Disaster Events](https://www.ncei.noaa.gov/access/billions/time-series/US/cost)
* [Global Average Surface Temperatures Monthly, and Global Land and Ocean Average Temperature Anomalies](https://github.com/datasets/global-temp)

I built a small desktop application in Python to load, clean and visualize the data, answer two key questions about climate change, and deepen my experience with data-driven GUI development.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the data set, the questions and answers, the code running and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

**Question 1:  How did global annual surface temperature anomalies evolve from 1980 through 2023?
>We compute the annual means of the monthly anomalies, re-based to the 1980-2010 baseline.
>**Result:** A steady upward trend from -0.13°C in 1980 to +0.75°C in 2023 increasing by 0.88°C over the period.

**Question 2: How did the annual count of U.S. billion-dollar disasters change from 1980–2023?
> We tally each year’s total events (droughts, floods, storms, etc.).
> **Result:** The average annual disaster count rose from 3 in 1980 to 27 in 2023 increasing by 24.

# Development Environment

**Python 3.13** in a virtual environment was used for development in Visual Studio Code.
Key libraries used:
**Pandas** for data loading & cleaning
**Matplotlib** for plotting
**CustomTkinter** for building the GUI
**pytest** for automated testing

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)
* [CustomTkinter Guide](https://github.com/TomSchimansky/CustomTkinter)

# Future Work

* Implement toggles to show/hide individual disaster types or regional subsets
* Implement toggles to show/hide individual disaster types or regional subsets
* Provide “Export to CSV/PDF” functionality for the charts
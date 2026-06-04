import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


# 1. ENTER YOUR DATA HERE
# Replace these examples with your actual dates ('YYYY-MM-DD') and counts.
# Make sure the dates match up exactly with the counts.
data = {
    "Date": [
        "2026-04-02",
        "2026-04-06",
        "2026-04-09",
        "2026-04-13",
        "2026-04-16",
        "2026-04-20",
        "2026-04-23",
        "2026-04-27",
        "2026-04-30",
        "2026-05-01",
        # ... Add the rest of your dates here following the same format
    ],
    "Moths": [
        1,
        2,
        4,
        8,
        12,
        22,
        35,
        48,
        52,
        47,
        # ... Add the rest of your 37 moth counts here
    ],
}

# 2. CONVERT DATA FOR PLOTTING
df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")  # Ensures dates are chronological

# Convert dates to numeric format (days since the start) so the smoother can read them
df["Date_Num"] = mdates.date2num(df["Date"])

# 3. APPLY LOWESS SMOOTHING
# 'frac' controls smoothness.
# A value of 0.3 means it uses a rolling window of 30% of your data points.
# Increase frac (e.g., 0.4) for a smoother line; decrease it (e.g., 0.2) for a more sensitive line.
lowess_feat = sm.nonparametric.lowess(df["Moths"], df["Date_Num"], frac=0.3)
df["Smoothed"] = lowess_feat[:, 1]

# 4. CREATE THE PLOT
plt.figure(figsize=(12, 6))

# Plot raw data as individual points (the &quot;noisy&quot; daily estimates)
plt.scatter(
    df["Date"],
    df["Moths"],
    color="gray",
    alpha=0.6,
    label="Daily Observation (Rough Estimate)",
    zorder=2,
)

# Plot the biological trend curve (the generations)
plt.plot(
    df["Date"],
    df["Smoothed"],
    color="darkgreen",
    linewidth=3,
    label="Population Trend (LOWESS)",
    zorder=3,
)

# 5. FORMAT THE CHART FOR SCANNABILITY
plt.title(
    "Moth Population Trends & Generational Peaks",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
plt.xlabel("Date", fontsize=12, labelpad=10)
plt.ylabel("Relative Abundance (Count Index)", fontsize=12, labelpad=10)

# Clean up date axis formatting
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.gca().xaxis.set_major_locator(
    mdates.WeekdayLocator(interval=1)
)  # Tick mark every week
plt.xticks(rotation=45)

plt.grid(True, linestyle="--", alpha=0.5, zorder=1)
plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
plt.tight_layout()

# Display the graph
plt.show()

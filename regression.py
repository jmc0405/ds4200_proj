import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# LOAD + CLEAN
# -------------------------
df = pd.read_csv("cleaned_music_data.csv")

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "How many hours of music do you listen to per day on average (estimated)?": "hours_listening",
    "How many concerts did you attend in 2025?": "concerts",
    "On average, how much did you spend on a concert ticket in 2025?": "avg_spend"
})

# Convert to numeric
df["hours_listening"] = pd.to_numeric(df["hours_listening"], errors="coerce")
df["concerts"] = pd.to_numeric(df["concerts"], errors="coerce")
df["avg_spend"] = pd.to_numeric(df["avg_spend"], errors="coerce")

df = df[(df["hours_listening"] >= 0) & (df["hours_listening"] <= 24)]

# Minimum concerts = 1
df["concerts"] = df["concerts"].apply(lambda x: 1 if pd.isna(x) or x <= 0 else x)

# Drop missing
df = df.dropna(subset=["hours_listening", "concerts", "avg_spend"])

# -------------------------
# REGRESSION PLOT
# (Spending vs Concerts)
# -------------------------
x = df["hours_listening"]
y = df["avg_spend"]

coef = np.polyfit(x, y, 1)
poly = np.poly1d(coef)

plt.figure()
plt.scatter(x, y)
plt.plot(x, poly(x))

plt.xlabel("Hours Listening per Day")
plt.ylabel("Average Ticket Spend ($)")
plt.title("Regression: Listening Time vs Spending")

plt.show()
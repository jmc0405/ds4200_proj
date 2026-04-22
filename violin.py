import pandas as pd
import plotly.express as px

# -------------------------
# LOAD + CLEAN
# -------------------------
df = pd.read_csv("cleaned_music_data.csv")
df.columns = df.columns.str.strip()

df = df.rename(columns={
    "School": "school",
    "How many hours of music do you listen to per day on average (estimated)?": "hours_listening"
})

df["hours_listening"] = pd.to_numeric(df["hours_listening"], errors="coerce")

# Keep realistic listening hours only
df = df[(df["hours_listening"] >= 0) & (df["hours_listening"] <= 24)]

# Drop missing schools / listening hours
df = df.dropna(subset=["school", "hours_listening"])

# Remove blank school labels
df = df[df["school"].astype(str).str.strip() != ""]

# -------------------------
# VIOLIN PLOT
# -------------------------
fig = px.violin(
    df,
    x="school",
    y="hours_listening",
    box=True,
    points="all",
    title="Distribution of Daily Music Listening Hours by School",
    labels={
        "school": "School",
        "hours_listening": "Hours Listening per Day"
    }
)

fig.update_layout(
    xaxis_tickangle=-20
)

fig.show()
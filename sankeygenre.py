import pandas as pd
import plotly.graph_objects as go
import statsmodels.api as sm
import re

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("cleaned_music_data.csv")

# -------------------------
# CLEAN COLUMN NAMES
# -------------------------
df.columns = df.columns.str.strip()

# Rename important columns
df = df.rename(columns={
    "Top Genre (#1)": "fav_genre",
    "What genres were the concerts you attended in 2025?": "concert_genre",
    "How many hours of music do you listen to per day on average (estimated)?": "hours_listening",
    "How many concerts did you attend in 2025?": "concerts",
    "On average, how much did you spend on a concert ticket in 2025?": "avg_spend"
})

# -------------------------
# CLEAN NUMERIC COLUMNS
# -------------------------
df["concerts"] = pd.to_numeric(df["concerts"], errors="coerce")
df["hours_listening"] = pd.to_numeric(df["hours_listening"], errors="coerce")
df["avg_spend"] = pd.to_numeric(df["avg_spend"], errors="coerce")

# Set minimum concerts attended to 1
df["concerts"] = df["concerts"].apply(lambda x: 1 if pd.isna(x) or x <= 0 else x)

# -------------------------
# CLEAN GENRE VALUES
# -------------------------
def clean_genre(x):
    if pd.isna(x):
        return None

    x = str(x).strip().lower()
    x = re.sub(r"\s+", " ", x)

    replacements = {
        "hip hop": "hip-hop",
        "hiphop": "hip-hop",
        "rap": "hip-hop",
        "rap/hip-hop": "hip-hop",
        "rnb": "r&b",
        "r&b": "r&b",
        "alt": "alternative",
        "alt rock": "alternative",
        "alternative rock": "alternative",
        "indie rock": "indie",
        "electronic": "edm",
        "edm/house": "edm",
        "pop music": "pop",
        "rock music": "rock"
    }

    cleaned = replacements.get(x, x)
    return cleaned.title()

df["fav_genre"] = df["fav_genre"].apply(clean_genre)

# Split multiple concert genres into separate rows
df["concert_genre"] = df["concert_genre"].astype(str).str.split(r",|/|;|&|\band\b", regex=True)
df = df.explode("concert_genre")
df["concert_genre"] = df["concert_genre"].apply(clean_genre)

# -------------------------
# REMOVE BAD / UNWANTED VALUES
# -------------------------
# Remove missing values
df = df.dropna(subset=["fav_genre", "concert_genre", "hours_listening", "concerts", "avg_spend"])

# Remove rock from left side
df = df[df["fav_genre"].str.lower() != "rock"]

# Remove bad values from right side
bad_right = ["nan", "a", "n", ""]
df = df[~df["concert_genre"].str.lower().isin(bad_right)]

# Remove very short junk values on right side
df = df[df["concert_genre"].str.len() > 1]

# -------------------------
# BUILD SANKEY DIAGRAM
# -------------------------
flow_counts = df.groupby(["fav_genre", "concert_genre"]).size().reset_index(name="count")

left_labels = sorted(flow_counts["fav_genre"].unique())
right_labels = sorted(flow_counts["concert_genre"].unique())

left_nodes = [f"Favorite: {g}" for g in left_labels]
right_nodes = [f"Concert: {g}" for g in right_labels]
all_nodes = left_nodes + right_nodes

label_to_index = {label: i for i, label in enumerate(all_nodes)}

flow_counts["source"] = flow_counts["fav_genre"].apply(lambda g: label_to_index[f"Favorite: {g}"])
flow_counts["target"] = flow_counts["concert_genre"].apply(lambda g: label_to_index[f"Concert: {g}"])

display_labels = left_labels + right_labels

fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20,
        thickness=20,
        label=display_labels
    ),
    link=dict(
        source=flow_counts["source"],
        target=flow_counts["target"],
        value=flow_counts["count"]
    )
)])

fig.update_layout(
    title_text="Favorite Genre to Concert Attendance Genre",
    font_size=11
)

fig.show()

# -------------------------
# REGRESSION
# Amount spent ~ hours listening + concerts attended
# -------------------------
X = df[["hours_listening", "concerts"]]
X = sm.add_constant(X)

y = df["avg_spend"]

model = sm.OLS(y, X).fit()

print(model.summary())
import os
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Global Weather Dashboard",
    layout="wide"
)

st.title("🌎 Global Weather Dashboard")
st.write("Explore weather data scraped from Time and Date.")

# Load data
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'data', 'weather_data.db')

conn = sqlite3.connect(db_path)

df = pd.read_sql_query(
    "SELECT * FROM global_weather",
    conn
)

conn.close()

# Sidebar filters
st.sidebar.header("Filters")

countries = sorted(df["country"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + countries
)

if selected_country != "All Countries":
    filtered_df = df[df["country"] == selected_country]
else:
    filtered_df = df

# Metrics
st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Cities",
    len(filtered_df)
)

col2.metric(
    "Average Temp (°F)",
    round(filtered_df["temperature_f"].mean(), 1)
)

col3.metric(
    "Maximum Temp (°F)",
    filtered_df["temperature_f"].max()
)

# Visualization 1
st.subheader("Top 10 Hottest Cities")

top_hot = (
    filtered_df
    .sort_values("temperature_f", ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(top_hot["city"], top_hot["temperature_f"])
ax.set_ylabel("Temperature (°F)")
ax.set_xlabel("City")
plt.xticks(rotation=45)

st.pyplot(fig)

# Visualization 2
st.subheader("Temperature Distribution")

fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.hist(filtered_df["temperature_f"], bins=10)
ax2.set_xlabel("Temperature (°F)")
ax2.set_ylabel("Frequency")

st.pyplot(fig2)

# Visualization 3
st.subheader("Weather Condition Counts")

condition_counts = (
    filtered_df["condition"]
    .value_counts()
)

fig3, ax3 = plt.subplots(figsize=(8,5))
condition_counts.plot(
    kind="bar",
    ax=ax3
)

ax3.set_xlabel("Condition")
ax3.set_ylabel("Count")

st.pyplot(fig3)
# Data table
st.subheader("Weather Data")

st.dataframe(filtered_df)

st.caption("Data source: timeanddate.com/weather")

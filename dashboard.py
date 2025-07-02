import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("final_data.csv")
df["Year"] = df["Year"].astype(str)

st.set_page_config(page_title="Saudi Economic Dashboard", layout="wide")
st.title("📊 Saudi Arabia Economic Insights Dashboard")

# KPI Cards
col1, col2, col3 = st.columns(3)

latest = df.iloc[-1]
col1.metric("GDP (US$)", f"${latest['GDP (US$)']:,}")
col2.metric("Inflation Rate (%)", f"{latest['Inflation (%)']:.2f}%")
col3.metric("Population", f"{int(latest['Population']):,}")

# Sidebar filter
year_range = st.slider("Select Year Range", int(df["Year"].min()), int(
    df["Year"].max()), (2010, int(df["Year"].max())))
filtered_df = df[(df["Year"].astype(int) >= year_range[0]) &
                 (df["Year"].astype(int) <= year_range[1])]

# Line chart
st.subheader("📈 GDP and Inflation Over Time")
fig = px.line(filtered_df, x="Year", y=[
              "GDP (US$)", "Inflation (%)"], markers=True)
st.plotly_chart(fig, use_container_width=True)

# Oil Rents
st.subheader("🛢️ Oil Rents as % of GDP")
fig2 = px.bar(filtered_df, x="Year", y="Oil Rents (% of GDP)",
              color="Oil Rents (% of GDP)", color_continuous_scale="Blues")
st.plotly_chart(fig2, use_container_width=True)

# Unemployment if available
if "Unemployment (%)" in df.columns:
    st.subheader("📉 Unemployment Trend (if available)")
    fig3 = px.line(df, x="Year", y="Unemployment (%)", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

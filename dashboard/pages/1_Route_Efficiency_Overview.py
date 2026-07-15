# import streamlit as st
# st.title("Route Efficiency Overview")
# st.write("Coming on Day 11")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🚚 Route Efficiency Overview")

@st.cache_data
def load_data():
    return pd.read_csv("MASTER_route_kpi_table.csv")

route_df = load_data()

st.sidebar.header("Filters")

factories = sorted(route_df["Factory"].unique())
selected_factories = st.sidebar.multiselect("Factory", factories, default=factories)

min_volume = st.sidebar.slider(
    "Minimum Route Volume",
    min_value=0,
    max_value=int(route_df["Route_Volume"].max()),
    value=0
)

filtered = route_df[
    (route_df["Factory"].isin(selected_factories)) &
    (route_df["Route_Volume"] >= min_volume)
]

st.subheader("Average Lead Time by Route")

chart_df = filtered.sort_values("Avg_Lead_Time")

fig = px.bar(
    chart_df,
    x="Avg_Lead_Time",
    y="Route",
    orientation="h",
    color="Factory",
    title="Average Lead Time by Route (lower is better)",
    labels={"Avg_Lead_Time": "Average Lead Time (days)", "Route": ""},
)
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Route Performance Leaderboard")

leaderboard = filtered.sort_values("Route_Efficiency_Score", ascending=False)[
    ["Efficiency_Rank","Route","Route_Volume","Avg_Lead_Time","Delay_Frequency_Pct","Route_Efficiency_Score"]
].rename(columns={
    "Efficiency_Rank": "Rank",
    "Route_Volume": "Shipments",
    "Avg_Lead_Time": "Avg Lead Time (days)",
    "Delay_Frequency_Pct": "Delay Rate (%)",
    "Route_Efficiency_Score": "Efficiency Score",
})

st.dataframe(
    leaderboard.style.format({
        "Avg Lead Time (days)": "{:.0f}",
        "Delay Rate (%)": "{:.1f}",
        "Efficiency Score": "{:.1f}",
    }),
    use_container_width=True,
    hide_index=True,
)

col1, col2 = st.columns(2)

with col1:
    st.success("🏆 Top 5 Most Efficient Routes")
    top5 = filtered.sort_values("Route_Efficiency_Score", ascending=False).head(5)
    for _, row in top5.iterrows():
        st.write(f"**{row['Route']}** -- {row['Avg_Lead_Time']:.0f} days avg, {row['Route_Volume']} shipments")

with col2:
    st.error("🐌 Bottom 5 Least Efficient Routes")
    bottom5 = filtered.sort_values("Route_Efficiency_Score", ascending=True).head(5)
    for _, row in bottom5.iterrows():
        st.write(f"**{row['Route']}** -- {row['Avg_Lead_Time']:.0f} days avg, {row['Route_Volume']} shipments")
import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🔍 Route Drill-Down")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

@st.cache_data
def load_data():
    return pd.read_csv(
        os.path.join(DASHBOARD_DIR, "order_level_data.csv"),
        parse_dates=["Order Date","Ship Date"]
    )

order_df = load_data()

st.sidebar.header("Drill-Down Filters")
min_date = order_df["Order Date"].min()
max_date = order_df["Order Date"].max()
date_range = st.sidebar.date_input(
    "Order Date Range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)
regions = sorted(order_df["Region"].unique())
selected_region = st.sidebar.selectbox("Region", ["All"] + regions)
if selected_region != "All":
    state_options = sorted(
        order_df[order_df["Region"]==selected_region]["State/Province"].unique()
    )
else:
    state_options = sorted(order_df["State/Province"].unique())
selected_state = st.sidebar.selectbox("State/Province", ["All"] + state_options)
ship_modes = sorted(order_df["Ship Mode"].unique())
selected_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)
max_lt = int(order_df["Lead Time"].max())
lt_threshold = st.sidebar.slider(
    "Show only orders with Lead Time above (days)", 0, max_lt, 0
)

filtered = order_df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        (filtered["Order Date"] >= pd.Timestamp(date_range[0])) &
        (filtered["Order Date"] <= pd.Timestamp(date_range[1]))
    ]
if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]
if selected_state != "All":
    filtered = filtered[filtered["State/Province"] == selected_state]
if selected_modes:
    filtered = filtered[filtered["Ship Mode"].isin(selected_modes)]
filtered = filtered[filtered["Lead Time"] >= lt_threshold]

st.write(f"Showing **{len(filtered):,}** of {len(order_df):,} total shipments.")

if filtered.empty:
    st.warning("No shipments match the current filters.")
    st.stop()

if selected_state != "All":
    st.subheader(f"Performance Detail: {selected_state}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Shipments", len(filtered))
    col2.metric("Avg Lead Time", f"{filtered['Lead Time'].mean():.0f} days")
    col3.metric("Total Sales", f"${filtered['Sales'].sum():,.2f}")
    by_factory = filtered.groupby("Factory").agg(
        Shipments=("Order ID","count"),
        Avg_Lead_Time=("Lead Time","mean")
    ).reset_index()
    fig = px.bar(by_factory, x="Factory", y="Avg_Lead_Time",
                 title=f"Avg Lead Time by Factory serving {selected_state}")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Order-Level Shipment Timeline")
timeline_fig = px.scatter(
    filtered.sort_values("Order Date"),
    x="Order Date", y="Lead Time", color="Ship Mode",
    hover_data=["Order ID","Product Name","City","State/Province"],
    title="Individual Shipments Over Time", opacity=0.6,
)
st.plotly_chart(timeline_fig, use_container_width=True)

with st.expander("View raw filtered data"):
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        csv, "filtered_shipments.csv", "text/csv"
    )

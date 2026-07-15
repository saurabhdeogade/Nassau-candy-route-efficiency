import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nassau Candy Route Efficiency", 
    layout="wide"
)

st.title("📦 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Dashboard")

st.markdown("""
Ye dashboard Nassau Candy Distributor ke 5 factories aur unke customer 
regions/states ke beech shipping route performance analyze karta hai.

Sidebar use karo alag pages ke beech navigate karne ke liye:
- **Route Efficiency Overview** -- route ke hisaab se average lead time aur leaderboard
- **Geographic Map** -- US heatmap shipping efficiency ka
- **Ship Mode Comparison** -- Standard vs Expedited shipping analysis
- **Route Drill-Down** -- state-level detail aur order-level timelines
""")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    route_df = pd.read_csv(os.path.join(BASE_DIR, "MASTER_route_kpi_table.csv"))
    order_df = pd.read_csv(
        os.path.join(BASE_DIR, "order_level_data.csv"),
        parse_dates=["Order Date", "Ship Date"]
    )
    return route_df, order_df

route_df, order_df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shipments", f"{len(order_df):,}")
col2.metric("Total Routes Tracked", f"{len(route_df)}")
col3.metric("Factories", order_df["Factory"].nunique())
col4.metric("States/Provinces Served", order_df["State/Province"].nunique())

st.info(
    "⚠️ Note: Is dashboard ke Lead Time figures directional hain. "
    "Data cleaning ke dauraan Ship Date field mein ek data quality issue "
    "mila tha -- absolute din-ginti ko literal mat maano, lekin "
    "route-to-route relative ranking meaningful hai."
)
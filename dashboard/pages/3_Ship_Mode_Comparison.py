import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📦 Ship Mode Comparison")

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/order_level_data.csv",
                      parse_dates=["Order Date","Ship Date"])

order_df = load_data()

mode_stats = order_df.groupby("Ship Mode").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipment_Count=("Order ID","count"),
    Avg_Sales=("Sales","mean"),
    Avg_Cost=("Cost","mean"),
).reset_index().sort_values("Avg_Lead_Time")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(
        mode_stats, x="Ship Mode", y="Avg_Lead_Time",
        title="Average Lead Time by Ship Mode",
        color="Ship Mode"
    )
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.bar(
        mode_stats, x="Ship Mode", y="Shipment_Count",
        title="Shipment Volume by Ship Mode",
        color="Ship Mode"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Cost vs Time Tradeoff")
fig3 = px.scatter(
    mode_stats,
    x="Avg_Lead_Time", y="Avg_Cost",
    size="Shipment_Count", color="Ship Mode", text="Ship Mode",
    labels={
        "Avg_Lead_Time":"Average Lead Time (days)",
        "Avg_Cost":"Average Cost ($)"
    },
    title="Does paying more actually buy a shorter lead time?",
)
fig3.update_traces(textposition="top center")
st.plotly_chart(fig3, use_container_width=True)

st.dataframe(
    mode_stats.style.format({
        "Avg_Lead_Time":"{:.0f}",
        "Avg_Sales":"${:.2f}",
        "Avg_Cost":"${:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.subheader("Standard vs Expedited Comparison")
order_df["Shipping_Tier"] = order_df["Ship Mode"].apply(
    lambda x: "Standard" if x == "Standard Class" else "Expedited"
)
tier_stats = order_df.groupby("Shipping_Tier").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Median_Lead_Time=("Lead Time","median"),
    Shipment_Count=("Order ID","count"),
).reset_index()
st.dataframe(tier_stats, use_container_width=True, hide_index=True)

diff = (
    tier_stats.loc[tier_stats["Shipping_Tier"]=="Expedited","Avg_Lead_Time"].values[0] -
    tier_stats.loc[tier_stats["Shipping_Tier"]=="Standard","Avg_Lead_Time"].values[0]
)
if diff > 0:
    st.warning(
        f"⚠️ Is dataset mein Expedited shipping, Standard se "
        f"{diff:.0f} days SLOWER nikli — koi clear speed advantage nahi mila."
    )
else:
    st.success(f"✅ Expedited shipping {abs(diff):.0f} days faster hai Standard se.")

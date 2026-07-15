import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🗺️ Geographic Shipping Map")

US_STATE_ABBR = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
    "Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC",
    "Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL",
    "Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA",
    "Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
    "Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT",
    "Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ",
    "New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND",
    "Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA",
    "Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN",
    "Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA",
    "West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY",
}

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/order_level_data.csv",
                      parse_dates=["Order Date","Ship Date"])

order_df = load_data()

state_perf = order_df.groupby("State/Province").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipment_Count=("Order ID","count"),
).reset_index()
state_perf["Abbr"] = state_perf["State/Province"].map(US_STATE_ABBR)
us_only = state_perf[state_perf["Abbr"].notnull()]
non_us = state_perf[state_perf["Abbr"].isnull()]

st.caption(f"Showing {len(us_only)} US states on map. "
           f"{len(non_us)} non-US provinces excluded.")

fig = px.choropleth(
    us_only, locations="Abbr", locationmode="USA-states",
    color="Avg_Lead_Time", scope="usa",
    color_continuous_scale="RdYlGn_r",
    labels={"Avg_Lead_Time":"Avg Lead Time (days)"},
    hover_data=["Shipment_Count"],
    title="Shipping Lead Time by State (Red=Slower, Green=Faster)",
)
fig.update_layout(height=550)
st.plotly_chart(fig, use_container_width=True)

if len(non_us) > 0:
    with st.expander("Non-US provinces excluded (data quality note)"):
        st.dataframe(
            non_us[["State/Province","Shipment_Count","Avg_Lead_Time"]],
            hide_index=True
        )

st.subheader("Regional Bottleneck Summary")
region_summary = order_df.groupby("Region").agg(
    Total_Shipments=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Total_Sales=("Sales","sum"),
).reset_index().sort_values("Avg_Lead_Time", ascending=False)

fig2 = px.bar(
    region_summary, x="Region", y="Avg_Lead_Time",
    color="Total_Shipments",
    title="Average Lead Time by Region (colored by shipment volume)",
    labels={"Avg_Lead_Time":"Avg Lead Time (days)"}
)
st.plotly_chart(fig2, use_container_width=True)
st.dataframe(region_summary, use_container_width=True, hide_index=True)

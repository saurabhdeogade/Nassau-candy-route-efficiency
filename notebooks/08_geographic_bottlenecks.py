import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv", parse_dates=["Order Date","Ship Date"])
route_state = pd.read_csv("E:/Un-Project File/nassau_project/outputs/04_route_state.csv")
print(df.shape, route_state.shape)

state_summary = df.groupby("State/Province").agg(
    Total_Shipments=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Total_Sales=("Sales","sum"),
).reset_index()

print(state_summary.sort_values("Total_Shipments", ascending=False).head(10))

volume_median = state_summary["Total_Shipments"].median()
leadtime_median = state_summary["Avg_Lead_Time"].median()

state_summary["High_Volume"] = state_summary["Total_Shipments"] > volume_median
state_summary["High_Lead_Time"] = state_summary["Avg_Lead_Time"] > leadtime_median
state_summary["Bottleneck"] = state_summary["High_Volume"] & state_summary["High_Lead_Time"]

print("Volume median:", volume_median)
print("Lead time median:", leadtime_median)

bottlenecks = state_summary[state_summary["Bottleneck"]].sort_values("Total_Shipments", ascending=False)
print("Bottleneck states:")
print(bottlenecks[["State/Province","Total_Shipments","Avg_Lead_Time"]])

region_summary = df.groupby("Region").agg(
    Total_Shipments=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Total_Sales=("Sales","sum"),
).reset_index().sort_values("Avg_Lead_Time", ascending=False)
print(region_summary)

total_shipments = state_summary["Total_Shipments"].sum()
state_summary["Pct_of_Total_Volume"] = 100 * state_summary["Total_Shipments"] / total_shipments
print(state_summary.sort_values("Pct_of_Total_Volume", ascending=False).head(10)[["State/Province","Total_Shipments","Pct_of_Total_Volume"]])

state_summary.to_csv("E:/Un-Project File/nassau_project/outputs/07_state_bottlenecks.csv", index=False)
region_summary.to_csv("E:/Un-Project File/nassau_project/outputs/07_region_summary.csv", index=False)
print()
print("Saved geographic bottleneck analysis")


import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv", parse_dates=["Order Date","Ship Date"])
print(df.shape)

delay_threshold = df["Lead Time"].quantile(0.75)
print("Delay threshold (75th percentile):", delay_threshold, "days")

df["Is_Delayed"] = df["Lead Time"] > delay_threshold

master = df.groupby(["Factory","Region"]).agg(
    Route_Volume=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Lead_Time_StdDev=("Lead Time","std"),
    Delay_Count=("Is_Delayed","sum"),
    Total_Sales=("Sales","sum"),
    Total_Gross_Profit=("Gross Profit","sum"),
).reset_index()

master["Route"] = master["Factory"] + " -> " + master["Region"]
master["Delay_Frequency_Pct"] = 100 * master["Delay_Count"] / master["Route_Volume"]

min_lt, max_lt = master["Avg_Lead_Time"].min(), master["Avg_Lead_Time"].max()
master["Route_Efficiency_Score"] = 100 * (max_lt - master["Avg_Lead_Time"]) / (max_lt - min_lt)

master = master.sort_values("Route_Efficiency_Score", ascending=False).reset_index(drop=True)
master["Efficiency_Rank"] = master.index + 1

print(master[["Efficiency_Rank","Route","Route_Volume","Avg_Lead_Time","Delay_Frequency_Pct","Route_Efficiency_Score"]])

factory_coords = {
    "Lot's O' Nuts":       (32.881893, -111.768036),
    "Wicked Choccy's":     (32.076176, -81.088371),
    "Sugar Shack":         (48.11914,  -96.18115),
    "Secret Factory":      (41.446333, -90.565487),
    "The Other Factory":   (35.1175,   -89.971107),
}
master["Factory_Lat"] = master["Factory"].map(lambda f: factory_coords[f][0])
master["Factory_Lon"] = master["Factory"].map(lambda f: factory_coords[f][1])

master["Lead_Time_Reliable"] = False
print(master.columns.tolist())

master.to_csv("E:/Un-Project File/nassau_project/outputs/MASTER_route_kpi_table.csv", index=False)
print()
print("Saved master KPI table:", master.shape)

master_state = df.groupby(["Factory","State/Province"]).agg(
    Route_Volume=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Lead_Time_StdDev=("Lead Time","std"),
    Delay_Count=("Is_Delayed","sum"),
    Total_Sales=("Sales","sum"),
).reset_index()

master_state["Route"] = master_state["Factory"] + " -> " + master_state["State/Province"]
master_state["Delay_Frequency_Pct"] = 100 * master_state["Delay_Count"] / master_state["Route_Volume"]
master_state["Lead_Time_Reliable"] = False

master_state.to_csv("E:/Un-Project File/nassau_project/outputs/MASTER_route_kpi_table_state.csv", index=False)
print("Saved state-level master table:", master_state.shape)

df.to_csv("E:/Un-Project File/nassau_project/outputs/04_full_order_level_final.csv", index=False)
print()
print("=== Day 9 complete: Master KPI tables ready ===")
import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv", parse_dates=["Order Date", "Ship Date"])
print(df.shape)

route_region = df.groupby(["Factory", "Region"]).agg(
    Total_Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean"),
    Lead_Time_StdDev=("Lead Time", "std"),
    Total_Sales=("Sales", "sum"),
    Total_Units=("Units", "sum"),
    Total_Gross_Profit=("Gross Profit", "sum"),
).reset_index()

route_region["Route"] = route_region["Factory"] + " -> " + route_region["Region"]

print(route_region.shape)
print(route_region.head())

route_state = df.groupby(["Factory", "State/Province"]).agg(
    Total_Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean"),
    Lead_Time_StdDev=("Lead Time", "std"),
    Total_Sales=("Sales", "sum"),
).reset_index()

route_state["Route"] = route_state["Factory"] + " -> " + route_state["State/Province"]

print(route_state.shape)

route_state["Low_Sample"] = route_state["Total_Shipments"] < 5
print("Routes with fewer than 5 shipments:", route_state["Low_Sample"].sum(), "out of", len(route_state))

route_region["Lead_Time_Reliable"] = False
route_state["Lead_Time_Reliable"] = False

route_region.to_csv("E:/Un-Project File/nassau_project/outputs/04_route_region.csv", index=False)
route_state.to_csv("E:/Un-Project File/nassau_project/outputs/04_route_state.csv", index=False)
print()
print("Saved both route-level tables")


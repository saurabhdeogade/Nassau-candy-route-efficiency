import pandas as pd

route_region = pd.read_csv("E:/Un-Project File/nassau_project/outputs/04_route_region.csv")
print(route_region.shape)

print(route_region[["Route","Avg_Lead_Time"]].sort_values("Avg_Lead_Time").to_string())

route_region_sorted = route_region.sort_values("Avg_Lead_Time", ascending=True).reset_index(drop=True)
route_region_sorted["Efficiency_Rank"] = route_region_sorted.index + 1

top_10 = route_region_sorted.head(10)
bottom_10 = route_region_sorted.tail(10)

print("TOP 10 MOST EFFICIENT ROUTES")
print(top_10[["Efficiency_Rank","Route","Avg_Lead_Time","Total_Shipments"]])
print()
print("BOTTOM 10 LEAST EFFICIENT ROUTES")
print(bottom_10[["Efficiency_Rank","Route","Avg_Lead_Time","Total_Shipments"]])

route_state = pd.read_csv("E:/Un-Project File/nassau_project/outputs/04_route_state.csv")

# Sirf wahi routes lo jisme kam se kam 5 shipments hain (Low Sample wale hata do)
reliable_routes = route_state[route_state["Total_Shipments"] >= 5].copy()
reliable_routes_sorted = reliable_routes.sort_values("Avg_Lead_Time")

top_10_state = reliable_routes_sorted.head(10)
bottom_10_state = reliable_routes_sorted.tail(10)

print("TOP 10 STATE-LEVEL ROUTES (reliable only)")
print(top_10_state[["Route","Avg_Lead_Time","Total_Shipments"]])
print()
print("BOTTOM 10 STATE-LEVEL ROUTES (reliable only)")
print(bottom_10_state[["Route","Avg_Lead_Time","Total_Shipments"]])

min_lt = route_region["Avg_Lead_Time"].min()
max_lt = route_region["Avg_Lead_Time"].max()

route_region["Route_Efficiency_Score"] = 100 * (max_lt - route_region["Avg_Lead_Time"]) / (max_lt - min_lt)
print(route_region[["Route","Avg_Lead_Time","Route_Efficiency_Score"]].sort_values("Route_Efficiency_Score", ascending=False))

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv")
ship_mode_perf = df.groupby("Ship Mode").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipment_Count=("Order ID","count"),
    Avg_Sales=("Sales","mean"),
).sort_values("Avg_Lead_Time")
print(ship_mode_perf)

route_region_sorted.to_csv("E:/Un-Project File/nassau_project/outputs/05_route_region_ranked.csv", index=False)
reliable_routes_sorted.to_csv("E:/Un-Project File/nassau_project/outputs/05_route_state_ranked.csv", index=False)
ship_mode_perf.to_csv("E:/Un-Project File/nassau_project/outputs/05_ship_mode_performance.csv")
print()
print("Saved all benchmarking tables")
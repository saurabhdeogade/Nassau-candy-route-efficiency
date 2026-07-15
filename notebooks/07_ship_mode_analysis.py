import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv", parse_dates=["Order Date","Ship Date"])
print(df.shape)

df["Shipping_Tier"] = df["Ship Mode"].apply(
    lambda x: "Standard" if x == "Standard Class" else "Expedited"
)
print(df["Shipping_Tier"].value_counts())

tier_comparison = df.groupby("Shipping_Tier").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Median_Lead_Time=("Lead Time","median"),
    Avg_Sales_Per_Order=("Sales","mean"),
    Avg_Cost_Per_Order=("Cost","mean"),
    Shipment_Count=("Order ID","count"),
)
print(tier_comparison)

ship_mode_detail = df.groupby("Ship Mode").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Lead_Time_StdDev=("Lead Time","std"),
    Shipment_Count=("Order ID","count"),
    Avg_Sales=("Sales","mean"),
).sort_values("Avg_Lead_Time")
print(ship_mode_detail)

mode_region = df.groupby(["Region","Ship Mode"]).agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipment_Count=("Order ID","count")
).reset_index()
print(mode_region.sort_values(["Region","Avg_Lead_Time"]))

tier_comparison.to_csv("E:/Un-Project File/nassau_project/outputs/06_shipping_tier_comparison.csv")
ship_mode_detail.to_csv("E:/Un-Project File/nassau_project/outputs/06_ship_mode_detail.csv")
mode_region.to_csv("E:/Un-Project File/nassau_project/outputs/06_mode_by_region.csv", index=False)
print()
print("Saved ship mode analysis outputs")


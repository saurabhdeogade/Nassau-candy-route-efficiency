import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/02_cleaned.csv", parse_dates=["Order Date", "Ship Date"])
print(df.shape)

print(df["Lead Time"].describe())

df["Route_Region"] = df["Factory"] + " -> " + df["Region"]
df["Route_State"] = df["Factory"] + " -> " + df["State/Province"]

print(df["Route_Region"].nunique(), "unique Factory->Region routes")
print(df["Route_State"].nunique(), "unique Factory->State routes")
print()
print(df["Route_Region"].value_counts().head(10))

print(df["Ship Mode"].value_counts())

df["Profit_Margin_Pct"] = (df["Gross Profit"] / df["Sales"]) * 100
print(df["Profit_Margin_Pct"].describe())

df.to_csv("E:/Un-Project File/nassau_project/outputs/03_features.csv", index=False)
print()
print("Saved:", df.shape)

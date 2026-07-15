import pandas as pd

df = pd.read_csv("E:/Un-Project File/nassau_project/outputs/01_with_factory.csv")
print(df.shape)

df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")

print("Order Date range:", df["Order Date"].min(), "to", df["Order Date"].max())
print("Ship Date range:", df["Ship Date"].min(), "to", df["Ship Date"].max())

df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
print(df["Lead Time"].describe())

print()
print("Order Date years:")
print(df["Order Date"].dt.year.value_counts().sort_index())
print()
print("Ship Date years:")
print(df["Ship Date"].dt.year.value_counts().sort_index())

# print(df[["Order Date", "Ship Date"]].sample(10))

for col in ["City", "State/Province", "Region", "Country/Region"]:
    df[col] = df[col].astype(str).str.strip()

print("Unique Regions:", sorted(df["Region"].unique()))
print("Number of unique States/Provinces:", df["State/Province"].nunique())

canada_provinces = ["Alberta", "British Columbia", "Manitoba", "Ontario", "Quebec",
                    "Saskatchewan", "Nova Scotia", "New Brunswick"]
df["Geo_Flag"] = df["State/Province"].isin(canada_provinces)
print("Rows with mismatched country/province:", df["Geo_Flag"].sum())

print()
print("Missing values per column:")
print(df.isnull().sum())
print()
print("Fully duplicated rows:", df.duplicated().sum())
print("Duplicated Order+Product combos:", df.duplicated(subset=["Order ID","Product ID"]).sum())

print()
print("Rows where Sales <= 0:", (df["Sales"] <= 0).sum())
print("Rows where Units <= 0:", (df["Units"] <= 0).sum())
print("Rows where Cost <= 0:", (df["Cost"] <= 0).sum())

implied = df["Sales"] - df["Cost"]
mismatch = (implied - df["Gross Profit"]).abs() > 0.01
print("Gross Profit formula mismatches:", mismatch.sum())

df.to_csv("E:/Un-Project File/nassau_project/outputs/02_cleaned.csv", index=False)
print()
print("Saved cleaned dataset:", df.shape)
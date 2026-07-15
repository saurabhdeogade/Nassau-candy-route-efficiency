import pandas as pd

# Factory coordinates (project brief se liya gaya)
factory_coords = {
    "Lot's O' Nuts":       (32.881893, -111.768036),
    "Wicked Choccy's":     (32.076176, -81.088371),
    "Sugar Shack":         (48.11914,  -96.18115),
    "Secret Factory":      (41.446333, -90.565487),
    "The Other Factory":   (35.1175,   -89.971107),
}

factory_df = pd.DataFrame([
    {"Factory": k, "Latitude": v[0], "Longitude": v[1]}
    for k, v in factory_coords.items()
])

print(factory_df)

product_to_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows":         "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious":    "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate":        "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy":                       "Sugar Shack",
    "SweeTARTS":                         "Sugar Shack",
    "Nerds":                             "Sugar Shack",
    "Fun Dip":                           "Sugar Shack",
    "Fizzy Lifting Drinks":              "Sugar Shack",
    "Everlasting Gobstopper":            "Secret Factory",
    "Lickable Wallpaper":                "Secret Factory",
    "Wonka Gum":                         "Secret Factory",
    "Hair Toffee":                       "The Other Factory",
    "Kazookles":                         "The Other Factory",
}

df = pd.read_csv("E:/Un-Project File/nassau_project/data/Nassau_Candy_Distributor.csv")
df["Factory"] = df["Product Name"].map(product_to_factory)

print(df[["Product Name", "Factory"]].head(10))

missing = df[df["Factory"].isnull()]
print()
print("Rows with no Factory mapped:", len(missing))
if len(missing) > 0:
    print(missing["Product Name"].unique())

df = df.merge(factory_df, on="Factory", how="left")
print(df[["Factory", "Latitude", "Longitude"]].drop_duplicates())    

df.to_csv("E:/Un-Project File/nassau_project/outputs/01_with_factory.csv", index=False)
print()
print("Saved:", df.shape)
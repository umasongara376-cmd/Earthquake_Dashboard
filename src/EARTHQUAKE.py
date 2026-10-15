import requests
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Fetch latest earthquake data from USGS
# --------------------------------------------------

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()


# --------------------------------------------------
# 2. Extract useful dashboard columns
# --------------------------------------------------

rows = []

for earthquake in data["features"]:

    properties = earthquake.get("properties", {})
    coordinates = earthquake.get("geometry", {}).get("coordinates", [])

    rows.append({
        "Earthquake_ID": earthquake.get("id"),

        "Magnitude": properties.get("mag"),
        "Place": properties.get("place"),

        "DateTime_UTC": pd.to_datetime(
            properties.get("time"),
            unit="ms",
            utc=True
        ),

        "Updated_UTC": pd.to_datetime(
            properties.get("updated"),
            unit="ms",
            utc=True
        ),

        "Depth_km": coordinates[2] if len(coordinates) > 2 else None,
        "Longitude": coordinates[0] if len(coordinates) > 0 else None,
        "Latitude": coordinates[1] if len(coordinates) > 1 else None,

        "Earthquake_Type": properties.get("type"),
        "Status": properties.get("status"),
        "Tsunami": properties.get("tsunami"),
        "Significance": properties.get("sig"),
        "Alert_Level": properties.get("alert"),

        "Magnitude_Source": properties.get("magSource"),
        "Location_Source": properties.get("locationSource"),

        "USGS_URL": properties.get("url")
    })


# --------------------------------------------------
# 3. Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(rows)


# --------------------------------------------------
# 4. Create time columns for Power BI
# --------------------------------------------------

df["Date"] = df["DateTime_UTC"].dt.date
df["Year"] = df["DateTime_UTC"].dt.year
df["Month"] = df["DateTime_UTC"].dt.month
df["Month_Name"] = df["DateTime_UTC"].dt.month_name()
df["Day"] = df["DateTime_UTC"].dt.day
df["Hour"] = df["DateTime_UTC"].dt.hour


# --------------------------------------------------
# 5. Sort latest earthquakes first
# --------------------------------------------------

df = df.sort_values(
    by="DateTime_UTC",
    ascending=False
).reset_index(drop=True)


# --------------------------------------------------
# 6. Save CSV
# --------------------------------------------------

output_path = Path("data/earthquake_data.csv")

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 7. Confirmation
# --------------------------------------------------

print("\nEarthquake data fetched successfully!")
print(f"Total records : {len(df):,}")
print(f"CSV saved at  : {output_path}")
print(f"Latest record : {df['DateTime_UTC'].max()}")
print(f"Oldest record : {df['DateTime_UTC'].min()}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())
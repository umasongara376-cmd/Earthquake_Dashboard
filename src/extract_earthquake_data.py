import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --------------------------------------------------
# 1. Date Range
# --------------------------------------------------

end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=365)

print(f"Fetching earthquakes from {start_date.date()} to {end_date.date()}")

# --------------------------------------------------
# 2. USGS API
# --------------------------------------------------

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []

current_start = start_date

# --------------------------------------------------
# 3. Fetch Data Month by Month
# --------------------------------------------------

while current_start < end_date:

    current_end = min(
        current_start + timedelta(days=30),
        end_date
    )

    print(
        f"\nFetching: "
        f"{current_start.date()} to {current_end.date()}"
    )

    params = {
        "format": "geojson",
        "starttime": current_start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": current_end.strftime("%Y-%m-%dT%H:%M:%S"),
        "eventtype": "earthquake",
        "orderby": "time",
        "limit": 20000
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    features = data.get("features", [])

    print(f"Records received: {len(features)}")

    # --------------------------------------------------
    # 4. Extract Records
    # --------------------------------------------------

    for feature in features:

        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        coordinates = geometry.get(
            "coordinates",
            [None, None, None]
        )

        all_records.append({
            "Earthquake_ID": feature.get("id"),

            "Magnitude": properties.get("mag"),

            "Place": properties.get("place"),

            "DateTime_UTC": pd.to_datetime(
                properties.get("time"),
                unit="ms",
                errors="coerce"
            ),

            "Updated_UTC": pd.to_datetime(
                properties.get("updated"),
                unit="ms",
                errors="coerce"
            ),

            "Depth_km": coordinates[2],

            "Longitude": coordinates[0],

            "Latitude": coordinates[1],

            "Earthquake_Type": properties.get("type"),

            "Status": properties.get("status"),

            "Tsunami": properties.get("tsunami"),

            "Significance": properties.get("sig"),

            "Alert_Level": properties.get("alert"),

            "Magnitude_Source": properties.get("magSource"),

            "Location_Source": properties.get("locationSource"),

            "USGS_URL": properties.get("url")
        })

    # Move to next period
    current_start = current_end


# --------------------------------------------------
# 5. Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(all_records)

# --------------------------------------------------
# 6. Remove Duplicate Earthquake IDs
# --------------------------------------------------

df = df.drop_duplicates(
    subset="Earthquake_ID"
).reset_index(drop=True)

# --------------------------------------------------
# 7. Create Date Columns
# --------------------------------------------------

df["Date"] = df["DateTime_UTC"].dt.date
df["Year"] = df["DateTime_UTC"].dt.year
df["Month"] = df["DateTime_UTC"].dt.month
df["Month_Name"] = df["DateTime_UTC"].dt.month_name()
df["Day"] = df["DateTime_UTC"].dt.day
df["Hour"] = df["DateTime_UTC"].dt.hour

# --------------------------------------------------
# 8. Save CSV
# --------------------------------------------------

output_path = Path("data/earthquake_data_1year.csv")

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)

# --------------------------------------------------
# 9. Final Information
# --------------------------------------------------

print("\n" + "=" * 50)
print("EXTRACTION COMPLETED")
print("=" * 50)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print(
    f"Date range: "
    f"{df['DateTime_UTC'].min()} "
    f"to "
    f"{df['DateTime_UTC'].max()}"
)

print(f"Duplicate IDs: {df['Earthquake_ID'].duplicated().sum()}")

print(f"Saved to: {output_path}")
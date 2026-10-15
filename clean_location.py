import pandas as pd
from pathlib import Path
import re

# --------------------------------------------------
# 1. Read Original Earthquake Data
# --------------------------------------------------

input_path = Path("data/earthquake_data_1year.csv")

df = pd.read_csv(input_path)

print(f"Original rows: {len(df)}")


# --------------------------------------------------
# 2. Create Short Location Function
# --------------------------------------------------

def create_short_location(place):

    if pd.isna(place):
        return None

    place = str(place).strip()

    # Remove common ending word "region"
    place = re.sub(
        r"\s+region$",
        "",
        place,
        flags=re.IGNORECASE
    ).strip()

    # Pattern:
    # "62 km WNW of Ninilchik, Alaska"
    # "6 km SE of Fredonia, Arizona"
    # "114 km NNE of Arctic Village, Alaska"
    #
    # We keep only the location after "of".

    match = re.search(
        r"\b\d+(?:\.\d+)?\s*km\s+[A-Za-z]+\s+of\s+(.+)$",
        place,
        flags=re.IGNORECASE
    )

    if match:
        location = match.group(1).strip()
        return location

    # For locations without the distance/direction format,
    # keep the cleaned original location.
    return place


# --------------------------------------------------
# 3. Create Dashboard-Friendly Location
# --------------------------------------------------

df["Location_Short"] = df["Place"].apply(
    create_short_location
)


# --------------------------------------------------
# 4. Save Cleaned Location Data
# --------------------------------------------------

output_path = Path("data/earthquake_data_location_cleaned.csv")

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 5. Check Results
# --------------------------------------------------

print("\nLocation cleaning completed!")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nSample results:")
print(
    df[["Place", "Location_Short"]]
    .head(15)
    .to_string(index=False)
)

print(f"\nSaved to: {output_path}")
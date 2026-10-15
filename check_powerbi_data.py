import pandas as pd
from pathlib import Path


# ============================================================
# POWER BI DATASET FINAL QUALITY CHECK
# ============================================================

file_path = Path("data/earthquake_data_powerbi.csv")

print("=" * 60)
print("POWER BI DATASET QUALITY CHECK")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(file_path)

print("\n--- BASIC STRUCTURE ---")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. DUPLICATE CHECK
# ------------------------------------------------------------

print("\n--- DUPLICATE CHECK ---")

duplicate_rows = df.duplicated().sum()
duplicate_ids = df["Earthquake_ID"].duplicated().sum()

print(f"Duplicate rows: {duplicate_rows}")
print(f"Duplicate Earthquake IDs: {duplicate_ids}")


# ------------------------------------------------------------
# 3. MISSING VALUES
# ------------------------------------------------------------

print("\n--- MISSING VALUES ---")

missing_values = df.isna().sum()
missing_values = missing_values[missing_values > 0]

if len(missing_values) == 0:
    print("No missing values found.")
else:
    print(missing_values)

print(f"Total missing cells: {df.isna().sum().sum()}")


# ------------------------------------------------------------
# 4. DATETIME CHECK
# ------------------------------------------------------------

print("\n--- DATETIME CHECK ---")

df["DateTime_UTC"] = pd.to_datetime(
    df["DateTime_UTC"],
    errors="coerce"
)

# IMPORTANT:
# Date is stored as DD-MM-YYYY
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

invalid_datetime = df["DateTime_UTC"].isna().sum()
invalid_date = df["Date"].isna().sum()

print(f"Invalid DateTime: {invalid_datetime}")
print(f"Invalid Date: {invalid_date}")

print(f"Minimum DateTime: {df['DateTime_UTC'].min()}")
print(f"Maximum DateTime: {df['DateTime_UTC'].max()}")


# ------------------------------------------------------------
# 5. COORDINATE CHECK
# ------------------------------------------------------------

print("\n--- COORDINATE CHECK ---")

invalid_latitude = (
    (df["Latitude"] < -90) |
    (df["Latitude"] > 90)
).sum()

invalid_longitude = (
    (df["Longitude"] < -180) |
    (df["Longitude"] > 180)
).sum()

print(f"Invalid Latitude: {invalid_latitude}")
print(f"Invalid Longitude: {invalid_longitude}")


# ------------------------------------------------------------
# 6. MAGNITUDE CHECK
# ------------------------------------------------------------

print("\n--- MAGNITUDE CHECK ---")

print(f"Minimum Magnitude: {df['Magnitude'].min()}")
print(f"Maximum Magnitude: {df['Magnitude'].max()}")
print(f"Missing Magnitude: {df['Magnitude'].isna().sum()}")
print(f"Magnitude > 10: {(df['Magnitude'] > 10).sum()}")


# ------------------------------------------------------------
# 7. DEPTH CHECK
# ------------------------------------------------------------

print("\n--- DEPTH CHECK ---")

print(f"Minimum Depth: {df['Depth_km'].min()}")
print(f"Maximum Depth: {df['Depth_km'].max()}")


# ------------------------------------------------------------
# 8. TSUNAMI CHECK
# ------------------------------------------------------------

print("\n--- TSUNAMI CHECK ---")

print(df["Tsunami"].value_counts(dropna=False))


# ------------------------------------------------------------
# 9. ALERT LEVEL CHECK
# ------------------------------------------------------------

print("\n--- ALERT LEVEL CHECK ---")

print(df["Alert_Level"].value_counts(dropna=False))


# ------------------------------------------------------------
# 10. LOCATION CHECK
# ------------------------------------------------------------

print("\n--- LOCATION CHECK ---")

missing_place = df["Place"].isna().sum()
missing_location_short = df["Location_Short"].isna().sum()
unique_locations = df["Location_Short"].nunique()

print(f"Missing Place: {missing_place}")
print(f"Missing Location_Short: {missing_location_short}")
print(f"Unique Location_Short: {unique_locations}")


# ------------------------------------------------------------
# 11. TIME COLUMN CHECK
# ------------------------------------------------------------

print("\n--- TIME COLUMN CHECK ---")

print(f"Year range: {df['Year'].min()} to {df['Year'].max()}")
print(f"Month range: {df['Month'].min()} to {df['Month'].max()}")
print(f"Day range: {df['Day'].min()} to {df['Day'].max()}")
print(f"Hour range: {df['Hour'].min()} to {df['Hour'].max()}")


# ------------------------------------------------------------
# 12. REQUIRED COLUMNS CHECK
# ------------------------------------------------------------

print("\n--- REQUIRED COLUMNS CHECK ---")

required_columns = [
    "Earthquake_ID",
    "Magnitude",
    "Place",
    "DateTime_UTC",
    "Depth_km",
    "Longitude",
    "Latitude",
    "Status",
    "Tsunami",
    "Significance",
    "Alert_Level",
    "USGS_URL",
    "Date",
    "Year",
    "Month",
    "Month_Name",
    "Day",
    "Hour",
    "Location_Short"
]

missing_required_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_required_columns:
    print("Missing required columns:")
    print(missing_required_columns)
else:
    print("All required columns are present.")


# ------------------------------------------------------------
# 13. FINAL PASS / FAIL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

checks = {
    "Row count": len(df) > 0,
    "Duplicate rows": duplicate_rows == 0,
    "Duplicate Earthquake IDs": duplicate_ids == 0,
    "Invalid DateTime": invalid_datetime == 0,
    "Invalid Date": invalid_date == 0,
    "Invalid Latitude": invalid_latitude == 0,
    "Invalid Longitude": invalid_longitude == 0,
    "Missing Magnitude": df["Magnitude"].isna().sum() == 0,
    "Magnitude > 10": (df["Magnitude"] > 10).sum() == 0,
    "Missing Place": missing_place == 0,
    "Missing Location_Short": missing_location_short == 0,
    "Required columns": len(missing_required_columns) == 0
}


all_passed = True

for check_name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{status}: {check_name}")

    if not result:
        all_passed = False


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

print("\n" + "=" * 60)

if all_passed:
    print("FINAL QA PASSED")
    print("Dataset is ready for Power BI.")
else:
    print("FINAL QA FAILED")
    print("Please review the failed checks.")

print("=" * 60)
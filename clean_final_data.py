import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Load location-cleaned data
# -----------------------------
input_path = Path("data/earthquake_data_location_cleaned.csv")

df = pd.read_csv(input_path)

print("Original shape:", df.shape)


# -----------------------------
# 2. Remove rows with missing Magnitude
# -----------------------------
missing_magnitude = df["Magnitude"].isna().sum()

df = df.dropna(subset=["Magnitude"])

print("Missing Magnitude rows removed:", missing_magnitude)


# -----------------------------
# 3. Remove unnecessary columns
# -----------------------------
columns_to_drop = [
    "Magnitude_Source",
    "Location_Source"
]

df = df.drop(columns=columns_to_drop)


# -----------------------------
# 4. Convert DateTime columns
# -----------------------------
df["DateTime_UTC"] = pd.to_datetime(df["DateTime_UTC"], errors="coerce")
df["Updated_UTC"] = pd.to_datetime(df["Updated_UTC"], errors="coerce")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# -----------------------------
# 5. Basic validation
# -----------------------------

print("\n--- Validation ---")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Earthquake IDs:", df["Earthquake_ID"].duplicated().sum())

print("Missing Magnitude:", df["Magnitude"].isna().sum())
print("Missing DateTime:", df["DateTime_UTC"].isna().sum())
print("Missing Latitude:", df["Latitude"].isna().sum())
print("Missing Longitude:", df["Longitude"].isna().sum())

print("Invalid Latitude:",
      ((df["Latitude"] < -90) | (df["Latitude"] > 90)).sum())

print("Invalid Longitude:",
      ((df["Longitude"] < -180) | (df["Longitude"] > 180)).sum())


# -----------------------------
# 6. Save final dataset
# -----------------------------
output_path = Path("data/earthquake_data_final.csv")

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nFinal cleaning completed!")
print("Final shape:", df.shape)
print("Saved to:", output_path)
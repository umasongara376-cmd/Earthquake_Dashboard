import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. Load current final dataset
# -----------------------------------
input_path = Path("data/earthquake_data_final.csv")

df = pd.read_csv(input_path)

print("Original shape:", df.shape)


# -----------------------------------
# 2. Clean Place whitespace
# -----------------------------------
df["Place"] = df["Place"].str.strip()
df["Location_Short"] = df["Location_Short"].str.strip()


# -----------------------------------
# 3. Reconstruct DateTime_UTC
# -----------------------------------

# Date is stored as DD-MM-YYYY
date_part = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# DateTime_UTC currently contains MM:SS.s
time_part = df["DateTime_UTC"].str.extract(
    r"^(?P<minute>\d{2}):(?P<second>\d{2})(?:\.(?P<fraction>\d+))?$"
)

minute = pd.to_numeric(time_part["minute"], errors="coerce")
second = pd.to_numeric(time_part["second"], errors="coerce")

fraction = (
    pd.to_numeric(
        "0." + time_part["fraction"].fillna("0"),
        errors="coerce"
    )
)

total_seconds = (
    minute * 60
    + second
    + fraction
)

df["DateTime_UTC"] = (
    date_part
    + pd.to_timedelta(df["Hour"], unit="h")
    + pd.to_timedelta(total_seconds, unit="s")
)


# -----------------------------------
# 4. Remove incomplete Updated_UTC
# -----------------------------------

df = df.drop(columns=["Updated_UTC"])


# -----------------------------------
# 5. Remove constant Earthquake_Type
# -----------------------------------

df = df.drop(columns=["Earthquake_Type"])


# -----------------------------------
# 6. Final validation
# -----------------------------------

print("\n--- Final Validation ---")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Earthquake IDs:",
      df["Earthquake_ID"].duplicated().sum())

print("Missing DateTime:",
      df["DateTime_UTC"].isna().sum())

print("Missing Magnitude:",
      df["Magnitude"].isna().sum())

print("Missing Latitude:",
      df["Latitude"].isna().sum())

print("Missing Longitude:",
      df["Longitude"].isna().sum())

print("Invalid Latitude:",
      ((df["Latitude"] < -90) | (df["Latitude"] > 90)).sum())

print("Invalid Longitude:",
      ((df["Longitude"] < -180) | (df["Longitude"] > 180)).sum())


# -----------------------------------
# 7. Check reconstructed datetime
# -----------------------------------

print("\nDateTime range:")
print("From:", df["DateTime_UTC"].min())
print("To:", df["DateTime_UTC"].max())


# -----------------------------------
# 8. Save Power BI ready dataset
# -----------------------------------

output_path = Path("data/earthquake_data_powerbi.csv")

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nFinal Power BI dataset created!")
print("Final shape:", df.shape)
print("Saved to:", output_path)
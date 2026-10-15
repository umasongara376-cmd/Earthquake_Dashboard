from pathlib import Path
import tempfile
import requests
import pandas as pd
import geopandas as gpd

# --------------------------------------------------
# 1. Find the input CSV
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

possible_files = [
    BASE_DIR / "data" / "earthquake_data_powerbi.csv",
    BASE_DIR / "earthquake_data_powerbi.csv",
    BASE_DIR.parent / "data" / "earthquake_data_powerbi.csv",
]

INPUT_FILE = next((p for p in possible_files if p.exists()), None)

if INPUT_FILE is None:
    raise FileNotFoundError(
        "earthquake_data_powerbi.csv nahi mili. "
        "CSV ko country.py ke folder mein ya uske data folder mein rakho."
    )

OUTPUT_FILE = INPUT_FILE.parent / "earthquake_data_with_country.csv"

# Earthquake ke nearest country se maximum distance: 300 km
MAX_DISTANCE_METERS = 300_000

# Natural Earth country boundary dataset
COUNTRY_URL = (
    "https://naturalearth.s3.amazonaws.com/"
    "10m_cultural/ne_10m_admin_0_countries.zip"
)


def main():
    print("Reading earthquake data...")

    df = pd.read_csv(INPUT_FILE)

    required_columns = {"Latitude", "Longitude"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"CSV mein required columns nahi hain: {sorted(missing_columns)}"
        )

    # Preserve original row order and all existing columns
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    valid = (
        df["Latitude"].between(-90, 90)
        & df["Longitude"].between(-180, 180)
    )

    # Invalid coordinates do not get assigned a guessed country
    df["Country"] = "Other"

    if not valid.any():
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print(f"Done. Output saved: {OUTPUT_FILE}")
        return

    print("Downloading country boundaries...")

    response = requests.get(COUNTRY_URL, timeout=120)
    response.raise_for_status()

    # Save downloaded ZIP temporarily so GeoPandas can read it
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = Path(temp_dir) / "countries.zip"
        zip_path.write_bytes(response.content)

        countries = gpd.read_file(f"zip://{zip_path}")

        if "ADMIN" not in countries.columns:
            raise ValueError(
                "Country boundary file mein ADMIN column nahi mila."
            )

        countries = countries[["ADMIN", "geometry"]].copy()
        countries = countries[
            countries.geometry.notna() & ~countries.geometry.is_empty
        ].to_crs("EPSG:8857")

        # Only rows with valid coordinates are processed
        points_df = df.loc[valid, ["Longitude", "Latitude"]].copy()
        points_df["_row_id"] = points_df.index

        points = gpd.GeoDataFrame(
            points_df,
            geometry=gpd.points_from_xy(
                points_df["Longitude"],
                points_df["Latitude"]
            ),
            crs="EPSG:4326",
        ).to_crs("EPSG:8857")

        print("Matching earthquakes with country boundaries...")

        nearest = gpd.sjoin_nearest(
            points,
            countries,
            how="left",
            max_distance=MAX_DISTANCE_METERS,
            distance_col="Distance_Meters",
        )

        # A boundary can occasionally match multiple equally near countries.
        # Keep one country assignment for each original row.
        nearest = nearest.sort_values(
            ["_row_id", "Distance_Meters"]
        ).drop_duplicates(subset="_row_id", keep="first")

        assigned = nearest.set_index("_row_id")["ADMIN"]

        # A nearby country is assigned within 300 km.
        # Far-away ocean locations remain "Other".
        df.loc[assigned.index, "Country"] = (
            assigned.fillna("Other").astype(str)
        )

    # Restore original coordinate values if numeric conversion changed them;
    # keep the original dataset columns and add only Country.
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\nCountry assignment completed.")
    print(f"Input rows: {len(df):,}")
    print(f"Output file: {OUTPUT_FILE}")
    print("\nCountry counts:")
    print(df["Country"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
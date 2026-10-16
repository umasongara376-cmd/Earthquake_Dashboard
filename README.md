# Earthquake Dashboard

A data preparation and visualization project for exploring earthquake records with a Power BI dashboard. The repository includes a Power BI report, CSV data files, and Python scripts for cleaning and preparing earthquake data.

## Repository Structure

- `dashboard/Earthquake_Dashboard.pbix` — Power BI report.
- `dashboard/dashboard images/` — dashboard preview assets, where included.
- `data/earthquake_data.csv`, `data/earthquake_data_1year.csv`, and other CSV files — source and intermediate dataset versions.
- `clean_location.py` — creates a shorter location field and writes `data/earthquake_data_location_cleaned.csv` from `data/earthquake_data_1year.csv`.
- `clean_final_data.py` — removes records with missing magnitude, drops source columns, converts date fields, and validates the cleaned data before saving the next dataset stage.
- `check_powerbi_data.py` — checks Power BI data, based on the script name; inspect the script for exact checks and expected paths.
- `country.py` — uses geographic data and latitude/longitude to assign a nearby country where a valid match is found.
- `Row Labels.txt` — supporting text data.

## Tools

- Microsoft Power BI Desktop
- Python 3
- pandas
- requests and GeoPandas for the country-assignment script

Install Python dependencies as needed:

```bash
python -m pip install pandas requests geopandas
```

## View the Dashboard

1. Download or clone the repository.
2. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/).
3. Open `dashboard/Earthquake_Dashboard.pbix`.
4. Review the report pages, filters, and visuals. If Power BI requests a data source, reconnect it to the appropriate local dataset before refreshing.

## Data Preparation Workflow

The repository contains multiple CSV versions, including one-year, location-cleaned, and final datasets. The scripts use specific relative paths, so run them from the repository root and confirm each expected input file exists before running a step.

A typical order based on the current script inputs is:

1. Prepare or place the one-year source CSV at `data/earthquake_data_1year.csv`.
2. Run `python clean_location.py` to create the location-cleaned CSV.
3. Run `python clean_final_data.py` after confirming its input path matches the output from the previous step.
4. Run `country.py` only when its expected input CSV is available and its geographic dependencies are installed.
5. Open the Power BI file and refresh only after verifying the report's data source.

## Data Quality Checks

The cleaning code checks fields such as magnitude, timestamps, latitude, longitude, duplicate rows, duplicate earthquake IDs, and coordinate ranges. Review the scripts to understand which dataset version each check applies to.

## Important Notes

- There are several similarly named CSV files. Keep track of which one is the raw, intermediate, and final dataset.
- Some scripts expect specific filenames that may not match every current data file; confirm paths before executing the full pipeline.
- The dashboard is a visualization and analysis project, not an earthquake early-warning or prediction system.
- Dataset coverage, source, and final analytical findings should be documented after verifying the data and report.

## License

No license is specified. Check the source dataset terms and contact the repository owner before redistributing project data or files.
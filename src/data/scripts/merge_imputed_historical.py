"""
Merge imputed values from ChicagoEnergyBenchmarking_Imputed.csv into the historical
benchmarking data (benchmarking-all-years.csv).

For any missing values in the historical data, check if an imputed value exists and add it
along with a flag indicating it was imputed.

This runs as part of the data pipeline after clean_and_split_data creates the initial
historical dataset.
"""

import pandas as pd
import json
from pathlib import Path


def run():
    """Merge imputed data into the historical benchmarking dataset."""

    # File paths
    historical_path = Path("src/data/dist/benchmarking-all-years.csv")
    imputed_path = Path("src/data/source/ChicagoEnergyBenchmarking_Imputed.csv")
    original_path = Path("src/data/source/ChicagoEnergyBenchmarking.csv")
    buildings_path = Path("src/data/dist/building-benchmarks.csv")
    output_path = historical_path  # Overwrite the historical file

    print("Loading historical benchmarking data...")
    df_historical = pd.read_csv(historical_path)

    print("Loading imputed data...")
    df_imputed = pd.read_csv(imputed_path)

    print("Loading original data...")
    df_original = pd.read_csv(original_path)

    print("Loading building data for names...")
    df_buildings = pd.read_csv(buildings_path)
    # Create a lookup dictionary for building ID -> name
    building_names = dict(zip(df_buildings['ID'].astype(str), df_buildings['PropertyName']))

    print(f"Historical data: {len(df_historical)} rows")
    print(f"Imputed data: {len(df_imputed)} rows")
    print(f"Original data: {len(df_original)} rows")
    print(f"Buildings data: {len(df_buildings)} rows")

    # Mapping from historical column names (GraphQL-formatted) to both imputed (snake_case)
    # and original column names (with spaces)
    column_mapping = {
        "ElectricityUse": {
            "imputed": "electricity_use_kbtu",
            "original": "Electricity Use (kBtu)"
        },
        "NaturalGasUse": {
            "imputed": "natural_gas_use_kbtu",
            "original": "Natural Gas Use (kBtu)"
        },
        "TotalGHGEmissions": {
            "imputed": "total_ghg_emissions_metric_tons_co2e",
            "original": "Total GHG Emissions (Metric Tons CO2e)"
        },
        "GHGIntensity": {
            "imputed": "ghg_intensity_kg_co2e_sq_ft",
            "original": "GHG Intensity (kg CO2e/sq ft)"
        },
        "SourceEUI": {
            "imputed": "source_eui_kbtu_sq_ft",
            "original": "Source EUI (kBtu/sq ft)"
        },
        "SiteEUI": {
            "imputed": "site_eui_kbtu_sq_ft",
            "original": "Site EUI (kBtu/sq ft)"
        },
        "DistrictSteamUse": {
            "imputed": "district_steam_use_kbtu",
            "original": "District Steam Use (kBtu)"
        },
        "DistrictChilledWaterUse": {
            "imputed": "district_chilled_water_use_kbtu",
            "original": "District Chilled Water Use (kBtu)"
        },
    }

    # Mapping for neighbor contribution columns (these contain JSON arrays)
    neighbor_column_mapping = {
        "NeighborsElectricityUse": "neighbors_electricity_use_kbtu",
        "NeighborsNaturalGasUse": "neighbors_natural_gas_use_kbtu",
        "NeighborsTotalGHGEmissions": "neighbors_total_ghg_emissions_metric_tons_co2e",
    }

    # Create a column to track which fields were imputed (comma-separated)
    df_historical["ImputedFields"] = ""

    # Initialize neighbor contribution columns as strings to hold JSON
    for hist_col in neighbor_column_mapping.keys():
        df_historical[hist_col] = ""

    # Create merge keys for comparison
    # Original CSV uses "Data Year" with a space
    df_original['merge_key'] = df_original['ID'].astype(str) + '_' + df_original['Data Year'].astype(int).astype(str)
    df_imputed['merge_key'] = df_imputed['id'].astype(str) + '_' + df_imputed['data_year'].astype(int).astype(str)
    df_historical['merge_key'] = df_historical['ID'].astype(str) + '_' + df_historical['DataYear'].astype(int).astype(str)

    # For each row in historical data, check which fields were imputed
    print("\nIdentifying imputed fields...")
    imputed_count = 0

    for idx, hist_row in df_historical.iterrows():
        merge_key = hist_row['merge_key']

        # Find corresponding rows in original and imputed data
        orig_rows = df_original[df_original['merge_key'] == merge_key]
        imp_rows = df_imputed[df_imputed['merge_key'] == merge_key]

        if len(imp_rows) == 0:
            continue

        imp_row = imp_rows.iloc[0]
        imputed_fields = []

        # Check each field to see if it was imputed
        for hist_col, col_names in column_mapping.items():
            orig_col = col_names["original"]
            imp_col = col_names["imputed"]

            # If original data is missing this value but imputed has it
            if len(orig_rows) > 0:
                orig_row = orig_rows.iloc[0]
                orig_value = orig_row.get(orig_col)
                imp_value = imp_row.get(imp_col)

                # Check if original was null/NaN but imputed has a value
                if (pd.isna(orig_value) or orig_value == '') and pd.notna(imp_value):
                    imputed_fields.append(hist_col)
                    imputed_count += 1

                    # Update the historical value with the imputed value
                    df_historical.at[idx, hist_col] = imp_value
            else:
                # If row doesn't exist in original, check if imputed has value
                imp_value = imp_row.get(imp_col)
                if pd.notna(imp_value):
                    imputed_fields.append(hist_col)
                    imputed_count += 1
                    df_historical.at[idx, hist_col] = imp_value

        # Store comma-separated list of imputed fields
        if imputed_fields:
            df_historical.at[idx, 'ImputedFields'] = ','.join(imputed_fields)

            # Add neighbor contribution data as JSON strings, enriched with building names
            for hist_col, imp_col in neighbor_column_mapping.items():
                neighbor_data = imp_row.get(imp_col)
                if pd.notna(neighbor_data) and neighbor_data:
                    try:
                        # Parse the JSON to enrich with building names
                        neighbors = json.loads(str(neighbor_data))
                        if isinstance(neighbors, list):
                            # Add building name to each neighbor
                            for neighbor in neighbors:
                                building_id = str(neighbor.get('building_id', ''))
                                neighbor['building_name'] = building_names.get(building_id, f'Building {building_id}')
                            # Store the enriched JSON
                            df_historical.at[idx, hist_col] = json.dumps(neighbors)
                        else:
                            # If not a list, store as-is
                            df_historical.at[idx, hist_col] = str(neighbor_data)
                    except (json.JSONDecodeError, Exception) as e:
                        # If parsing fails, store the original
                        print(f"  Warning: Failed to parse neighbor data for row {idx}: {e}")
                        df_historical.at[idx, hist_col] = str(neighbor_data)

    print(f"  Identified {imputed_count} imputed field values")

    # Count how many rows had at least one imputed field
    imputed_rows = (df_historical["ImputedFields"] != "").sum()

    # Drop the temporary merge key
    df_historical = df_historical.drop(columns=['merge_key'])

    # Save the merged data
    print(f"\nTotal values imputed: {imputed_count}")
    print(f"Rows with imputed data: {imputed_rows}")
    print(f"Saving to {output_path}...")
    df_historical.to_csv(output_path, index=False)
    print("Done!")


if __name__ == "__main__":
    run()

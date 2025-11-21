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
import math


def clean_value_for_json(value):
    """Convert pandas NaN/None to None for valid JSON serialization."""
    if pd.isna(value) or (isinstance(value, float) and math.isnan(value)):
        return None
    # Also handle the string "nan" that pandas sometimes produces
    if isinstance(value, str) and value.lower() == 'nan':
        return None
    return value


def run():
    """Merge imputed data into the historical benchmarking dataset."""

    historical_path = Path("src/data/dist/benchmarking-all-years.csv")
    imputed_path = Path("src/data/source/ChicagoEnergyBenchmarking_Imputed.csv")
    original_path = Path("src/data/source/ChicagoEnergyBenchmarking.csv")
    buildings_path = Path("src/data/dist/building-benchmarks.csv")
    output_path = historical_path

    print("Loading historical benchmarking data...")
    df_historical = pd.read_csv(historical_path)

    print("Loading imputed data...")
    df_imputed = pd.read_csv(imputed_path)

    print("Loading original data...")
    df_original = pd.read_csv(original_path)

    print("Loading building data for neighbor lookups...")
    df_buildings = pd.read_csv(buildings_path)

    building_details_by_year = {}
    building_names_fallback = {}
    building_sqft_fallback = {}

    for _, row in df_original.iterrows():
        building_id = str(row['ID'])
        year = str(int(row['Data Year']))
        key = f"{building_id}_{year}"

        building_details_by_year[key] = {
            'name': row.get('Property Name', ''),
            'address': row.get('Address', ''),
            'property_type': row.get('Primary Property Type', ''),
            'square_footage': row.get('Gross Floor Area - Buildings (sq ft)', None),
            'year_built': row.get('Year Built', None),
            'electricity_use': row.get('Electricity Use (kBtu)', None),
            'natural_gas_use': row.get('Natural Gas Use (kBtu)', None),
            'total_ghg_emissions': row.get('Total GHG Emissions (Metric Tons CO2e)', None),
            'ghg_intensity': row.get('GHG Intensity (kg CO2e/sq ft)', None),
            'chicago_energy_rating': row.get('Chicago Energy Rating', None),
            'energy_star_score': row.get('ENERGY STAR Score', None),
            'ward': row.get('Ward', None),
            'community_area': row.get('Community Area', ''),
        }

        property_name = row.get('Property Name', '')
        if pd.notna(property_name) and str(property_name).lower() != 'nan' and property_name != '':
            if building_id not in building_names_fallback:
                building_names_fallback[building_id] = {
                    'name': property_name,
                    'year': int(row['Data Year'])
                }
            else:
                if int(row['Data Year']) > building_names_fallback[building_id]['year']:
                    building_names_fallback[building_id] = {
                        'name': property_name,
                        'year': int(row['Data Year'])
                    }

        square_footage = row.get('Gross Floor Area - Buildings (sq ft)')
        if pd.notna(square_footage):
            if building_id not in building_sqft_fallback:
                building_sqft_fallback[building_id] = square_footage
            else:
                if int(row['Data Year']) > building_names_fallback.get(building_id, {}).get('year', 0):
                    building_sqft_fallback[building_id] = square_footage

    print(f"Historical data: {len(df_historical)} rows")
    print(f"Imputed data: {len(df_imputed)} rows")
    print(f"Original data: {len(df_original)} rows")
    print(f"Buildings data: {len(df_buildings)} rows")

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

    neighbor_column_mapping = {
        "NeighborsElectricityUse": "neighbors_electricity_use_kbtu",
        "NeighborsNaturalGasUse": "neighbors_natural_gas_use_kbtu",
        "NeighborsTotalGHGEmissions": "neighbors_total_ghg_emissions_metric_tons_co2e",
    }

    df_historical["ImputedFields"] = ""

    for hist_col in neighbor_column_mapping.keys():
        df_historical[hist_col] = ""

    df_original['merge_key'] = df_original['ID'].astype(str) + '_' + df_original['Data Year'].astype(int).astype(str)
    df_imputed['merge_key'] = df_imputed['id'].astype(str) + '_' + df_imputed['data_year'].astype(int).astype(str)
    df_historical['merge_key'] = df_historical['ID'].astype(str) + '_' + df_historical['DataYear'].astype(int).astype(str)

    print("\nIdentifying imputed fields...")
    imputed_count = 0

    for idx, hist_row in df_historical.iterrows():
        merge_key = hist_row['merge_key']

        orig_rows = df_original[df_original['merge_key'] == merge_key]
        imp_rows = df_imputed[df_imputed['merge_key'] == merge_key]

        if len(imp_rows) == 0:
            continue

        imp_row = imp_rows.iloc[0]
        imputed_fields = []

        for hist_col, col_names in column_mapping.items():
            orig_col = col_names["original"]
            imp_col = col_names["imputed"]

            if len(orig_rows) > 0:
                orig_row = orig_rows.iloc[0]
                orig_value = orig_row.get(orig_col)
                imp_value = imp_row.get(imp_col)

                if (pd.isna(orig_value) or orig_value == '') and pd.notna(imp_value):
                    imputed_fields.append(hist_col)
                    imputed_count += 1
                    df_historical.at[idx, hist_col] = imp_value
            else:
                imp_value = imp_row.get(imp_col)
                if pd.notna(imp_value):
                    imputed_fields.append(hist_col)
                    imputed_count += 1
                    df_historical.at[idx, hist_col] = imp_value

        if imputed_fields:
            df_historical.at[idx, 'ImputedFields'] = ','.join(imputed_fields)

            for hist_col, imp_col in neighbor_column_mapping.items():
                neighbor_data = imp_row.get(imp_col)
                if pd.notna(neighbor_data) and neighbor_data:
                    try:
                        neighbors = json.loads(str(neighbor_data))
                        if isinstance(neighbors, list):
                            current_year = str(int(hist_row['DataYear']))

                            for neighbor in neighbors:
                                neighbor_row_idx = neighbor.get('building_id', '')

                                try:
                                    row_idx = int(neighbor_row_idx)
                                    if 0 <= row_idx < len(df_imputed):
                                        actual_building_id = str(df_imputed.iloc[row_idx]['id'])
                                    else:
                                        actual_building_id = str(neighbor_row_idx)
                                except:
                                    actual_building_id = str(neighbor_row_idx)

                                neighbor['building_id'] = actual_building_id

                                lookup_key = f"{actual_building_id}_{current_year}"
                                details = building_details_by_year.get(lookup_key, {})

                                building_name = clean_value_for_json(details.get('name'))
                                name_from_year = None

                                if not building_name and actual_building_id in building_names_fallback:
                                    fallback_info = building_names_fallback[actual_building_id]
                                    building_name = fallback_info['name']
                                    name_from_year = fallback_info['year']

                                neighbor['building_name'] = building_name or f'Building {actual_building_id}'
                                neighbor['name_from_year'] = name_from_year
                                neighbor['address'] = clean_value_for_json(details.get('address', ''))
                                neighbor['property_type'] = clean_value_for_json(details.get('property_type', ''))

                                square_footage = clean_value_for_json(details.get('square_footage'))
                                if not square_footage and actual_building_id in building_sqft_fallback:
                                    square_footage = clean_value_for_json(building_sqft_fallback[actual_building_id])
                                neighbor['square_footage'] = square_footage
                                neighbor['year_built'] = clean_value_for_json(details.get('year_built'))
                                neighbor['electricity_use'] = clean_value_for_json(details.get('electricity_use'))
                                neighbor['natural_gas_use'] = clean_value_for_json(details.get('natural_gas_use'))
                                neighbor['total_ghg_emissions'] = clean_value_for_json(details.get('total_ghg_emissions'))
                                neighbor['ghg_intensity'] = clean_value_for_json(details.get('ghg_intensity'))
                                neighbor['chicago_energy_rating'] = clean_value_for_json(details.get('chicago_energy_rating'))
                                neighbor['energy_star_score'] = clean_value_for_json(details.get('energy_star_score'))
                                neighbor['ward'] = clean_value_for_json(details.get('ward'))
                                neighbor['community_area'] = clean_value_for_json(details.get('community_area', ''))

                            df_historical.at[idx, hist_col] = json.dumps(neighbors)
                        else:
                            df_historical.at[idx, hist_col] = str(neighbor_data)
                    except (json.JSONDecodeError, Exception) as e:
                        print(f"  Warning: Failed to parse neighbor data for row {idx}: {e}")
                        df_historical.at[idx, hist_col] = str(neighbor_data)

    print(f"  Identified {imputed_count} imputed field values")

    imputed_rows = (df_historical["ImputedFields"] != "").sum()
    df_historical = df_historical.drop(columns=['merge_key'])

    print(f"\nTotal values imputed: {imputed_count}")
    print(f"Rows with imputed data: {imputed_rows}")
    print(f"Saving to {output_path}...")
    df_historical.to_csv(output_path, index=False)
    print("Done!")


if __name__ == "__main__":
    run()

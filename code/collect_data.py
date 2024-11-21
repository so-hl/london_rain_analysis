# TO RUN: python collect_data.py ../data/world_cities.csv --london_daily_output ../data/london_daily_rain.csv --london_hourly_output ../data/london_hourly_rain.csv --all_daily_output ../data/all_daily_rain.csv --all_hourly_output ../data/all_hourly_rain.csv

import argparse
import json
import pandas as pd
import my_functions

# Load cities data
with open("../data/cities_config.json", "r") as file:
    cities_all = json.load(file)

# Define coordinates for London
coord_london = [51.50853, -0.12574]


def collect_data(coord_file):
    # Initialize coordinates for cities
    coord_all = my_functions.extract_coord(coord_file, cities_all, {})

    # Initialize results dictionary
    results_all = {}

    # Store results for London
    rain_data_london_daily, rain_data_london_hourly = my_functions.get_rain_data(
        coord_london[0], coord_london[1]
    )
    results_all["GB,London"] = {
        "daily": rain_data_london_daily["daily"],
        "hourly": rain_data_london_hourly["hourly"],
    }

    # Store results for other cities
    for cities in coord_all.values():
        for city, coord in cities.items():
            lat = float(coord[0])
            long = float(coord[1])
            rain_data_daily, rain_data_hourly = my_functions.get_rain_data(lat, long)
            results_all[city] = {
                "daily": rain_data_daily["daily"],
                "hourly": rain_data_hourly["hourly"],
            }

    return results_all


def process_city_data(city, data, data_type, container):
    df = pd.DataFrame(data[data_type])
    df["city"] = city
    container.append(df)


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Collect rainfall data for London and other cities."
    )
    parser.add_argument(
        "coord_file", help="Path to the CSV file containing city coordinates."
    )
    parser.add_argument(
        "--london_daily_output",
        default="../data/london_daily_rain.csv",
        help="Output CSV file for London's daily data (default: london_daily_rain.csv)",
    )
    parser.add_argument(
        "--london_hourly_output",
        default="../data/london_hourly_rain.csv",
        help="Output CSV file for London's hourly data (default: london_hourly_rain.csv)",
    )
    parser.add_argument(
        "--all_daily_output",
        default="../data/all_daily_rain.csv",
        help="Output CSV file for all cities' daily data (default: all_daily_rain.csv)",
    )
    parser.add_argument(
        "--all_hourly_output",
        default="../data/all_hourly_rain.csv",
        help="Output CSV file for all cities' hourly data (default: all_hourly_rain.csv)",
    )
    args = parser.parse_args()

    # Collect data
    results_all = collect_data(args.coord_file)

    # Save London's daily data to CSV
    london_daily_df = pd.DataFrame(results_all["GB,London"]["daily"])
    london_daily_df.to_csv(args.london_daily_output, index=False)
    print(f"London's daily data saved to {args.london_daily_output}")

    # Save London's hourly data to CSV
    london_hourly_df = pd.DataFrame(results_all["GB,London"]["hourly"])
    london_hourly_df.to_csv(args.london_hourly_output, index=False)
    print(f"London's hourly data saved to {args.london_hourly_output}")

    # Initialise empty lists to store cities dataframes
    cities_daily = []
    cities_hourly = []

    # Loop through each city in results_all
    for city, data in results_all.items():
        if city == "GB,London":
            continue
        process_city_data(city, data, "daily", cities_daily)
        process_city_data(city, data, "hourly", cities_hourly)

    # Save all cities' daily data to CSV
    cities_daily_df = pd.concat(cities_daily, ignore_index=True)
    cities_daily_df.to_csv(args.all_daily_output, index=False)
    print(f"All cities' daily data saved to {args.all_daily_output}")

    # Save all cities' hourly data to CSV
    cities_hourly_df = pd.concat(cities_hourly, ignore_index=True)
    cities_hourly_df.to_csv(args.all_hourly_output, index=False)
    print(f"All cities' hourly data saved to {args.all_hourly_output}")


if __name__ == "__main__":
    main()

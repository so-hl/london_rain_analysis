import json
import csv
import pandas as pd
from lets_plot import *
import ipywidgets as widgets
from IPython.display import display

# Load cities to region mapping
with open("../data/cities_config.json", "r") as file:
    cities_config = json.load(file)


def extract_coord(file, cities_all_dict, coord_all_dict):
    """
    FUNCTION:
    Extracts coordinates of cities from a CSV file into a dictionary mapped by region.
    -------------------------------------------------------------------------------------
    PARAMETERS:
    file : str
        Path to CSV containing city coordinates.
        CSV file should contain city name, region name, lattiude, longitude.
    cities_all_dict: dict
        Dictionary mapping regions to lists of cities.
    coord_all_dict: dict
        Dictionary to be updated with city coordinates.
    ----------------------------------------------------------------------
    RETURNS:
    dict
        The updated coord_all_dict with coordinates added for cities found in the input CSV file.
    """
    # Read CSV file and create city_coords dictionary
    with open(file, "r") as file:
        reader = csv.reader(file)
        city_coords = {f"{row[0]},{row[1]}": [row[2], row[3]] for row in reader}

    # Update coord_all_dict
    coord_all_dict = {
        region: {city: city_coords[city] for city in cities if city in city_coords}
        for region, cities in cities_all_dict.items()
    }

    return coord_all_dict


def rename_columns(df):
    """
    FUNCTION:
    Renames columns in DataFrame for clarity and consistency.
    --------------------------------------------------------
    PARAMETERS:
    df : pandas.DataFrame
        DataFrame whose columns are to be renamed.
        DataFrame should contain columns "rain_sum" and "time".
    --------------------------------------------------------
    RETURNS:
    None
        The DataFrame is modified and no value is returned.
    """
    df.rename(columns={"rain_sum": "rain", "time": "date"}, inplace=True)


def group_month(df):
    """
    FUNCTION:
    Groups DataFrame by month and city, summing the monthly amount of rainfall in each city.
    ----------------------------------------------------------------------------------------
    PARAMETERS:
    df : pandas.DataFrame
        DataFrame to be regrouped based on months and cities.
        DataFrame should contain at least "date" and "rain" columns.
    --------------------------------------------------------------
    RETURNS:
    pandas.DataFrame
        New DataFrame with columns "month", "city" and "rain",
        where "rain" contains total rainfall summed for each city per month.
    """
    df["month"] = df["date"].dt.to_period("M")
    monthly_df = df.groupby(["month", "city"])["rain"].sum().reset_index()
    monthly_df["date"] = monthly_df["month"].dt.to_timestamp()
    return monthly_df.drop(columns=["month"])


def map_region(city):
    """
    FUNCTION:
    Maps a city to its corresponding region.
    ----------------------------------------
    PARAMETERS:
    city : str
        Name of city to be mapped to its region.
    -------------------------------------------
    RETURNS:
    str
        Region associated with city.
    """
    for region, cities in cities_config.items():
        if city in cities:
            return region


# Function to calculate average rainfall overall
def calculate_average_rainfall(df, frequency="D"):
    """
    FUNCTION:
    Calculates average rainfall from DataFrame by
    (1) grouping DataFrame by the specified frequency and
    (2) computing average rainfall for the grouped entries
    and creates a new DataFrame with average rainfall per specified frequency.
    --------------------------------------------------------------------------
    PARAMETERS:
    df : pandas.DataFrame
        DataFrame containing "date" and "rain" columns.
    frequency : str, optional
        "D" for daily, "M" for monthly.
        "D" is set as default.
    --------------------------
    RETURNS:
    pandas.DataFrame
        New DataFrame with columns "date" and "rain", where "rain" is average rainfall
        per month or per day for each city.
    """
    # Group by specified frequency and calculate average rainfall
    if frequency == "M":
        average_df = group_month(df)
        average_df = average_df.groupby(["date"])["rain"].mean().reset_index()
    else:  # Default to daily
        average_df = df.groupby("date")["rain"].mean().reset_index()

    average_df["rain"] = average_df["rain"].round(2)
    average_df["city"] = "Average city"
    return average_df


def plot_rainfall(london_df, cities_df, title):
    """
    FUNCTION:
    Plots rainfall data for London and other cities by
    (1) combining rainfall data for London and other cities into a single DataFrame and
    (2) generating a line plot showing rainfall over time.
    ------------------------------------------------------
    PARAMETERS:
    london_df : pandas.DataFrame
        DataFrame contianing rainfall data for London with "date" and "rain" columns.
    cities_df : pandas.DataFrame
        DataFrame containing rainfall data for other cities with "date" and "rain" columns.
    title : str
        Title for graph.
    --------------------------
    RETURNS:
    ggplot
        ggplot object representing the line graph of rainfall data.
    """
    # Combine dataframes
    df_combined = pd.concat([london_df, cities_df])

    # Plot line graphs
    plot = (
        ggplot(df_combined, aes(x="date", y="rain", color="city"))
        + geom_line(size=0.8, alpha=0.7)
        + labs(title=title, x="Date", y="Rainfall (mm)", color="City")
        + ggsize(3000, 800)
        + theme(plot_title=element_text(size=20, face="bold", hjust=0.5))
        + scale_x_datetime(format="%b %Y")
    )
    return plot


def calculate_region_average_rainfall(df, frequency="D"):
    """
    FUNCTION:
    Calculate the average rainfall by region from the provided DataFrame by
    (1) mapping cities to their respective regions and
    (2) computing the average rainfall for each region based on specified frequency (daily or monthly)
    and creates a new DataFrame containing average rainfall values grouped by region and date.
    ------------------------------------------------------------------------------------------
    PARAMETERS:
    df : pandas.DataFrame
        DataFrame containing "date", "rain" and "city" columns
    frequency : str, optional
        "D" for daily, "M" for monthly.
        "D" is set as default.
    --------------------------
    RETURNS:
    pandas.DataFrame
        DataFrame with columns "date", "region", and "rain".
    """
    # Map city to region
    df["region"] = df["city"].apply(map_region)

    # Group by specified frequency and region
    if frequency == "M":
        average_df = group_month(df)
        average_df["region"] = average_df["city"].apply(map_region)
        average_df = average_df.groupby(["region", "date"])["rain"].mean().reset_index()
    else:  # Default to daily
        average_df = df.groupby(["date", "region"])["rain"].mean().reset_index()

    average_df["rain"] = average_df["rain"].round(2)
    return average_df


def plot_regional_rainfall(london_df, regions_df, selected_regions=None, frequency="D"):
    """
    FUNCTION:
    Plots rainfall data for London and other cities by
    (1) combining rainfall data for London and other cities based on regions into a single DataFrame and
    (2) generating a line plot showing rainfall over time.
    ------------------------------------------------------
    PARAMETERS:
    london_df : pandas.DataFrame
        DataFrame contianing rainfall data for London with "date" and "rain" columns.
    regions_df : pandas.DataFrame
        DataFrame containing regional rainfall data for other cities with "date", "rain" and "region" columns.
    frequency : str, optional
        "D" for daily, "M" for monthly.
        "D" is set as default.
    --------------------------
    RETURNS:
    ggplot
        ggplot object representing the line graph of rainfall data.
    """
    # Filter regions if specified and update city labels
    if selected_regions:
        regions_df = regions_df[regions_df["region"].isin(selected_regions)].assign(
            city=regions_df["region"].apply(lambda r: f"Average city in {r}")
        )
    else:
        regions_df = regions_df.assign(
            city=regions_df["region"].apply(lambda r: f"Average city in {r}")
        )
    df_combined = pd.concat([london_df, regions_df])

    # Titles
    if frequency == "M":
        title = "Monthly Rainfall Comparison"
    else:
        title = "Daily Rainfall Comparison"

    # Plot line graphs
    plot = (
        ggplot(df_combined, aes(x="date", y="rain", color="city"))
        + geom_line(size=0.8, alpha=0.7)
        + labs(
            title=title, subtitle="By Region", x="Date", y="Rainfall (mm)", color="City"
        )
        + ggsize(3000, 800)
        + theme(
            plot_title=element_text(size=20, face="bold", hjust=0.5),
            plot_subtitle=element_text(hjust=0.5),
        )
        + scale_x_datetime(format="%b %Y")
    )
    return plot


# Function to group by season
def group_season(df, city=True):  # set "city" as default
    """
    FUNCTION:
    Groups rainfall data by season and year, by city or region, and aggregates rainfall.
    ------------------------------------------------------------------------------------
    PARAMETERS:
    df : pandas.DataFrame
        DataFrame containing "date" and "rain" columns, with "city" or "region" columns.
    city : bool, optional
        if True: groups data by city; if False: groups data by region.
        Default is set to True.
    ----------------------------
    RETURNS:
    pandas.DataFrame
        DataFrame with columns "season", "year" and either "city" or "region",
        showing the total rainfall for each season.
    """
    seasons = {
        "Winter": ["December", "January", "February"],
        "Spring": ["March", "April", "May"],
        "Summer": ["June", "July", "August"],
        "Autumn": ["September", "October", "November"],
    }
    seasonal_df = df.copy()
    seasonal_df["month"] = seasonal_df["date"].dt.strftime("%B")
    seasonal_df["year"] = seasonal_df["date"].dt.strftime("%Y")

    # Determine season for each month
    seasonal_df["season"] = seasonal_df["month"].apply(
        lambda month: next(
            (season for season, months in seasons.items() if month in months), None
        )
    )

    # Group by season, year, and city, then sum rainfall
    group_cols = ["season", "year", "city"] if city else ["season", "year", "region"]
    seasonal_df = seasonal_df.groupby(group_cols)["rain"].sum().reset_index()
    seasonal_df["rain"] = seasonal_df["rain"].round(2)

    # Define the order of seasons
    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    seasonal_df["season"] = pd.Categorical(
        seasonal_df["season"], categories=season_order, ordered=True
    )

    # Sort the DataFrame by year and then by season
    seasonal_df.sort_values(by=["year", "season"], inplace=True)

    # Combine seasons and years for plotting
    seasonal_df["season_year"] = (
        seasonal_df["season"].astype(str) + " " + seasonal_df["year"].astype(str)
    )

    # Reset index
    seasonal_df.reset_index(drop=True, inplace=True)
    return seasonal_df


def raininess_rank(london, region):
    """
    FUNCTION:
    Ranks cities in different regions by their median rainfall in descending order.
    -------------------------------------------------------------------------------
    PARAMETERS:
    london : float
        Median rainfall value for London
    region : dict
        Dictionary with regions as keys and median rainfall values as values.
    -------------------------------------------------------------------------
    PRINTS:
    Ranked list of regions by their median rainfall in descending order.
    """
    # Add London's median rainfall to the dictionary for ranking
    region["London"] = london

    # Sort by descending amount of rain
    sorted_list = sorted(region.items(), key=lambda x: x[1], reverse=True)

    # Print the ranking
    print("Rainfall Ranking by Median Rainfall (in descending order):")
    for rank, (region, median_rainfall) in enumerate(sorted_list, start=1):
        if region == "London":
            print(f"{rank}. London: {median_rainfall:.2f}mm")
        else:
            print(f"{rank}. Average city in {region}: {median_rainfall:.2f}mm")

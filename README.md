# "Is London really as rainy as the movies make it out to be?"
Summative submitted and selected as the model repository for LSE DS105 Data for Data Science
Score: 95/100

## **1. About**

This project collects and analyses rainfall data globally to compare trends between London and other cities. The analysis and visualisations highlight patterns and anomalies in rainfall distribution. 


## **2. Installation**
This project requires Python 3.x. To install all necessary dependencies, simply run:

```bash
pip install -r requirements.txt
```


## **3. Usage**
Run `collect_data.py` from terminal with the following command:
```bash 
python collect_data.py ../data/world_cities.csv --london_daily_output ../data/london_daily_rain.csv --london_hourly_output ../data/london_hourly_rain.csv --all_daily_output ../data/all_daily_rain.csv --all_hourly_output ../data/all_hourly_rain.csv
```


## **4. Project Structure**
- `data_collection.py`: Collects rainfall data from [OpenMeTeo](https://open-meteo.com/)
- `analysis.ipynb`: Main Jupyter notebook for data analysis and visualisation
- `my_functions.py`: Script for all functions to be imported into Jupyter notebook
- `requirements.txt`: Text file containing all requirements necessary to run the project
- `data/`: Directory where collected data is stored as CSV files and additional data required for analysis is stored
- `README.md`: Project documentation


## **5. Data Sources**  
**[OpenMeteo's API](https://open-meteo.com/)** was used due to its (1) high-resolution data (2) detailed documentation (3) accessibility.  

`world_cities.csv` was also used to obtain the latitude and longitude of other cities. 
`cities_config.json` was used to map cities to their respective regions.


## **6. Methodology**
*Objective*: The analysis aimed to compare rainfall patterns of London to the average rainfall across various cities globally. Specifically, the analysis aimed to compare:
* London's daily, monthly, and seasonal rainfall against the global average.
* London's rainfall against the average rainfall of cities grouped by their geographic region (Africa, Asia, Europe, North America, Oceania, South America)

The **preliminary analysis** focused on visualising the data through plots.  

a. London vs. Global Average  
- Daily and Monthly Comparisons: To visually explore the differences in rainfall patterns between London and the global average, line graphs were used. These graphs clearly illustrate the trends in daily and monthly rainfall, highlighting how London’s rainfall varies compared to the global average over time.  
- Seasonal Comparison: For the seasonal analysis, a bar graph was chosen to better represent the differences in rainfall for each season. Bar graphs are useful in highlighting specific differences in rainfall volumes across seasons, making it easier to compare London's seasonal rainfall to the global average.

b. London vs. Regional Averages
- Regional Groupings: Cities were grouped by region (e.g., Oceania, Africa, Europe, etc.). For each region, average daily, monthly, and seasonal rainfall were calculated, and London’s rainfall was compared against these regional averages.  
- Interactive Plot for Regional Analysis: Given the large number of cities involved, the regional comparisons were displayed in an interactive plot. This allowed the user to select specific regions to view the relevant rainfall data for London and the selected region without overwhelming the viewer with too much information at once.  
- Interactivity: The interactive plot was designed to reduce clutter and make the analysis more user-friendly. By selecting a region from a dropdown menu, the plot updates dynamically to show London’s rainfall compared to that region’s average. This approach ensures a more organized and clear visualisation of the data.

The **further analysis** focused on calculating the median of various rainfall data across different time periods (daily, monthly, and seasonal). The median was chosen as it provides a robust measure of central tendency, particularly when comparing rainfall patterns. Unlike the mean, the median is less sensitive to extreme values, which makes it a better measure of comparison when addressing the question: "Is London rainier?" This is a question that cannot be explicitly answered from the graphs alone, as they may be influenced by occasional extreme rainfall events.

For the regional analysis, the median rainfall for each region was also calculated. To provide further insight, a raininess ranking was created based on the median rainfall values across the different regions. This ranking allowed for a clearer comparison of how London's rainfall stands relative to other regions, without the influence of outlier data points.


## **7. Points of consideration**
* **Time period**: 2019-2023 (data from the last 5 years)  
*Rationale*: Sufficient data to analyse trends, and recent enough to be indicative of London's raininess in recent years 

* **Global analysis**:      
40 cities, with a range from each region
*Rationale*: This allows for significant diversity in climates and geographical contexts, thus providing a comprehensive basis for comparison in this data analysis project. 

* **Measure of raininess**:     
**Amount of rain (mm)**     
This was identified as the key metric to define raininess in a city. 

* **Parameters used**   
rain_sum (daily rainfall)

* **Data Format**   
CSV was used to store the daily data, as it is more compatible than JSON for working with pandas.

* **Reformatting**      
[Black](https://black.readthedocs.io/en/stable/) was used to reformat the python files.
The VS Code reformatter was used to reformat the jupyter notebooks.


## **8. Expected Outputs and Results**  
- CSV files containing daily rainfall data for London and other cities
- Plots and databases comparing daily, monthly and seasonal rainfall trends in London versus other cities (the average city globally and the average city by region)
- Analysis of median rainfall and rankings of median rainfall


## **9. Future improvements**  
To define raininess more comprehensively, there is potential for future expansion through analysis of:
- Number of rainy days per month and per season  
- Number of hours of rain per month and per season  
- Number of hours of rain per month and per season (during the day)
to yield a more comprehensive metric of raininess.


## **Author**  
Vienna (So Hoi Ling), Year 1 LSE Econs student

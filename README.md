# San Francisco Real Estate Dashboard

This project takes a look at real estate data from San Francisco 2010-2016, focusing on sale prices and rental rates, with the idea of presenting what properties would potentially be worth buying to rent out.

## Repository guide
#### Starting Data (in [Data](https://github.com/redtea3930/real-estate-dashboard/tree/main/Data) folder):
* [neighborhoods_coordinates.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Data/neighborhoods_coordinates.csv) a small dataset of lat/long coordinates for named neighborhoods
* [sfo_neighborhoods_census_data.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Data/sfo_neighborhoods_census_data.csv) dataset of sales prices, number of housing units, and gross rent for named neighborhoods, sorted by year and neighborhood. Number of housing units and gross rent values are averages for each neighborhood by year.

#### Output Data (in [Output](https://github.com/redtea3930/real-estate-dashboard/tree/main/Output) folder):
* [yearly_avg-units.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/yearly_avg_units.csv) a small dataframe of average total housing units across all named neighborhoods by year. Project instructions were to create this file in the course of the project
* [concatenated.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/concatenated.csv) a concatenation of the inpu neighborhoods_coordinates.csv file with a processed version of the input sfo_neighborhoods_census_data.csv file. This file was created for visual analysis to determine data cleaning strategies while making the neighborhood map plot (see below)
* [Plots](https://github.com/redtea3930/real-estate-dashboard/tree/main/Output/Plots): a folder containing static files of plots created for this project, listed below by libraries used and file name:
    * Pandas
        * [yearly_avg_units.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/yearly_avg_units.png)
        * [price_plot.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/price_plot.png)
        * [rent_plot.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/rent_plot.png)
        * [price_and_rent_plot](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/price_and_rent_plot.png)
    * Holoviews
        * [average_price_by_neighborhood.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/average_price_by_neighborhood.png)
        * [average_rent_by_neighborhood.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/average_rent_by_neighborhood.png)
        * [top_10_neighborhoods.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/top_10_neighborhoods.png)
        * [top_10_sale_and_rent.png](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/top_10_sale_and_rent.png)
    * Plotly
        * [map_plot.html](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/map_plot.html)
        * [parallel_categories.html](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/parallel_categories.html)
        * [parallel_coordinates.html](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/parallel_coordinates.html)
        * [sunburst.html](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/Plots/sunburst.html) 

#### Code Files:
* [rental_analysis.ipynb](https://github.com/redtea3930/real-estate-dashboard/blob/main/rental_analysis.ipynb) a Python notebook with project instructions and initial coding, detailed in "Coding" section below.
* [dashboard.py](https://github.com/redtea3930/real-estate-dashboard/blob/main/dashboard.py) a Python script with finalized versions of plot coding and Streamlit dashboard code, detailed in "Dashboard" section below.

***

## Coding
From the supplied dataframes, several plots were contstructed:

#### Pandas Plots:
* yearly_avg_units groupby() unsed to group data by year; min(), max() and std() used to set y axis limits to show relevant scale.
* price_plot.png  rent_plot.png one column each from starter data extracted for groupby()
* price_and_rent_plot the above two plots combined into one plot with two y axes, using subplots() and twinx()

#### Holoviews Plots:

To export hvplot plots as png files, I installed selenium and Firefox geckodriver. Unfortunately I was only able to create static images without interactivity. I expect there is some way to export hvplots to HTML, but I was unable to determine how to do this.
* average_price_by_neighborhood.png hvplot kwarg "groupby", not to be confused with the pandas function
* average_rent_by_neighborhood.png  hvplot kwarg "groupby", not to be confused with the pandas function
* top_10_neighborhoods.png
* top_10_sale_and_rent.png grouped bar chart, created by simply running hvplot.bar() on a dataframe containing only columns for the x axis and two relevant columns to be plotted as bars

#### Plotly Plots:
* map_plot.html
    * concatenation: dataframe of lat/lon for named neighborhoods was concatenated to the census data. This unexpectedly left several neighborhoods and coordinates listed seperately, despite the neighborhood names being apparently spelled identically in the two source dataframes. There were also several neighborhoods with identical coordinates (eg Alamo Square, Financial Distict North, Financial Disctrict South, and South of Market). I opted to drop all nulls and leave co-located neighborhood coordinates as they were.
    * .env file: a previously issued API key for mapbox.com was stored to a .env file, which was saved in a .gitignore for data security. 
    * scatter_mapbox() was used to create a geographic scatter plot using the API key for mapbox access, the lat/lon data for locations, and census data for size/color of scatter points
* parallel_categories.html 
* parallel_coordinates.html
* sunburst.html

***

## Dashboard

A Streamlit dashboard with a selectbar to select any one of the created plots at a time in a dedicated sidebar. The scope of this project did not includ deploying this to the web, the dashboard can be accessed by running:
```
streamlit run dashboard.py 
```
from command line in a folder containing data from this repository.

The plots of average price and rent per year were put in columns

***

## Conclusions


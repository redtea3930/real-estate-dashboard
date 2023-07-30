# San Francisco Real Estate Dashboard

This project takes a look at real estate data from San Francisco 2010-2016, focusing on sale prices and rental rates, with the idea of presenting what properties would potentially be worth buying to rent out.

## Repository guide
Starting Data (in [Data](https://github.com/redtea3930/real-estate-dashboard/tree/main/Data) folder):
* [neighborhoods_coordinates.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Data/neighborhoods_coordinates.csv) a small dataset of lat/long coordinates for named neighborhoods
* [sfo_neighborhoods_census_data.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Data/sfo_neighborhoods_census_data.csv) dataset of sales prices, number of housing units, and gross rent for named neighborhoods, sorted by year and neighborhood. Number of housing units and gross rent values are averages for each neighborhood by year.

Output Data (in [Output](https://github.com/redtea3930/real-estate-dashboard/tree/main/Output) folder):
* [yearly_avg-units.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/yearly_avg_units.csv) a small dataframe of average total housing units across all named neighborhoods by year. Project instructions were to create this file in the course of the project
* [concatenated.csv](https://github.com/redtea3930/real-estate-dashboard/blob/main/Output/concatenated.csv) a concatenation of the inpu neighborhoods_coordinates.csv file with a processed version of the input sfo_neighborhoods_census_data.csv file. This file was created for visual analysis to determine data cleaning strategies while making the neighborhood map plot (see below)
* Plots a folder containing static files of plots created for this project, listed below by file name, libraries used, and techniques used:
    *

Code Files:
* [rental_analysis.ipynb](https://github.com/redtea3930/real-estate-dashboard/blob/main/rental_analysis.ipynb) a Python notebook with project instructions and initial coding, detailed in "Coding" section below.
* [dashboard.py](https://github.com/redtea3930/real-estate-dashboard/blob/main/dashboard.py) a Python script with finalized versions of plot coding and Streamlit dashboard code, detailed in "Dashboard" section below.

## Coding

## Dashboard

## Conclusions
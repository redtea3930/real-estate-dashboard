import streamlit as st
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv
import holoviews as hv
hv.extension('bokeh', logo=False)

# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("mapbox")
px.set_mapbox_access_token(map_box_api)

# Import the necessary CSVs to Pandas DataFrames
file_path = Path("Data/neighborhoods_coordinates.csv")
neighborhood_data = pd.read_csv(file_path)
neighborhood_data = neighborhood_data.rename(columns={'Neighborhood': 'neighborhood'}).set_index('neighborhood')

file_path = Path("Data/sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")

# Define Panel Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    yearly_avg_units = sfo_data['housing_units'].groupby('year').mean()
    min = yearly_avg_units.min()
    max = yearly_avg_units.max()
    std = yearly_avg_units.std()
    fig = plt.figure()
    yearly_avg_units.plot(kind='bar', 
                          xlabel='Year', 
                          ylim=[min-std, max+std],
                          title='Housing Units in San Francisco 2010-2016'
                         )
    return fig

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    rent_plot = sfo_data['gross_rent'].groupby('year').mean()
    fig = plt.figure()
    rent_plot.plot(ylabel='Gross Rent', 
                   marker='o', 
                   title='Average Gross Rent by Year', 
                   color='red'
                  )
    return fig

def average_sales_price():
    """Average Sales Price Per Year."""
    price_plot = sfo_data['sale_price_sqr_foot'].groupby('year').mean()
    fig = plt.figure()
    price_plot.plot(ylabel='Sale Price per SqFt',
                    marker='o', 
                    title='Average Sale Price per SqFt by Year'
                   )
    return fig

def average_price_by_neighborhood():
    """Average Prices by Neighborhood."""
    sfo_grouped = sfo_data.groupby(['year', 'neighborhood']).mean().reset_index()
    fig = sfo_grouped.hvplot.line(x='year',
                        xlabel='Year', 
                        y='sale_price_sqr_foot', 
                        ylabel='Mean Sale Price per Sq Ft',
                        groupby='neighborhood'
                       )
    return hv.render(fig)

def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    fig = top_10.hvplot.bar(x='neighborhood',
                  xlabel='Neighborhood',
                  rot=90,
                  y='sale_price_sqr_foot',
                  ylabel='Mean Sale Price per Sq Ft,',
                  title='Top 10 Most Expensive San Francisco Neighborhoods, Avg 2010-2016',
                  frame_width=600,
                  frame_height=250
                 )
    return hv.redner(fig)

def most_expensive_neighborhoods_rent_sales():
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    top_10_full =  sfo_data[sfo_data['neighborhood'].isin(top_10.neighborhood)]
    top_10_full_1 = top_10_full.drop(columns='housing_units').rename(columns={'sale_price_sqr_foot' : 'Mean Sales Price per Sq Ft', 'gross_rent' : 'Gross Rent' })
    fig = top_10_full_1.hvplot.bar(x='year', 
                       rot=90, 
                       groupby='neighborhood',
                       height=500,
                       title='Sale Price and Rent of 10 Most Expensive Neighborhoods, yearly 2010-2016' 
                      )
    return hv.render(fig)
    
def parallel_coordinates():
    """Parallel Coordinates Plot."""
    top_10['gross_rent'] = top_10['gross_rent'].round(2)
    top_10['sale_price_sqr_foot'] = top_10['sale_price_sqr_foot'].round(2)
    fig = px.parallel_coordinates(top_10,
                       dimensions=['sale_price_sqr_foot', 'housing_units', 'gross_rent'],
                       color='sale_price_sqr_foot',
                       color_continuous_scale=px.colors.sequential.Inferno,
                       labels={"sale_price_sqr_foot": "Sale Price per Sq Ft",
                               "housing_units": "Housing Units",
                               "gross_rent": 'Gross Rent'},)

def parallel_categories():
    """Parallel Categories Plot."""
    top_10['gross_rent'] = top_10['gross_rent'].round(2)
    top_10['sale_price_sqr_foot'] = top_10['sale_price_sqr_foot'].round(2)
    px.parallel_categories(top_10,
                       dimensions=['neighborhood', 'sale_price_sqr_foot', 'housing_units', 'gross_rent'],
                       color='sale_price_sqr_foot',
                       color_continuous_scale=px.colors.sequential.Inferno,
                       labels={"neighborhood": "Neighborhood",
                               "sale_price_sqr_foot": "Sale Price per Sq Ft",
                               "housing_units": "Housing Units",
                               "gross_rent": 'Gross Rent'}
                          )
                           
def neighborhood_map():
    """Neighborhood Map."""
    sfon = sfo_data.groupby('neighborhood').mean()
    sfo_location = pd.concat([neighborhood_data, sfon], axis=1)
    sfo_location = sfo_location.dropna()
    map_plot = px.scatter_mapbox(
        sfo_location,
        title='Mean Sale Price (marker size) and Gross Rent (marker color) in San Francisco',
        lat="Lat",
        lon="Lon",
        hover_name=sfo_location.index,
        #Coordinates removed from hover data, end users unlikely to want precise lat/lon
        hover_data={'Lat': False,
                    'Lon': False,
                   },
        size='sale_price_sqr_foot',
        size_max=15,
        color='gross_rent',
        color_continuous_scale='rainbow',
        zoom=10
    )

def sunburst():
    """Sunburst Plot."""
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    top_10_full =  sfo_data[sfo_data['neighborhood'].isin(top_10.neighborhood)]
    fig = px.sunburst(top_10_full,
                      path=[top_10_full.index, 'neighborhood'],
                      color='gross_rent',
                      color_continuous_scale='blues',
                 )
    return fig

# Start Streamlit App
st.header('San Francisco Rental Analysis Dashboard')

# pandas plot streamlit call
st.pyplot(housing_units_per_year())

# hvplot plot streamlit call
st.bokeh_chart(most_expensive_neighborhoods_rent_sales())

# plotly plot Streamlit call
st.plotly_chart(sunburst())

col1, col2, col3 = st.columns(3)

with col1:
   st.header("MXE")
   

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")
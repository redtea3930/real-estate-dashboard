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
                   xlabel='Year',
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
                    xlabel='Year',
                    marker='o', 
                    title='Average Sale Price per SqFt by Year'
                   )
    return fig

def average_rent_and_price():
    """Average Gross Rent and Sale Price on same plot"""
    # create subplot and right y axis objects with subplots() and twinx()
    fig,ax = plt.subplots()
    ax2=ax.twinx()
    
    # set labels for y axes
    ax.set_ylabel('Sale Price per SqFt', color='blue', fontsize = 14)
    ax2.set_ylabel('Gross Rent', color='red', fontsize = 14)
    
    # Sale price left y axis subplot with x axis label and title for full plot
    price_plot = sfo_data['sale_price_sqr_foot'].groupby('year').mean()
    price_plot.plot(title='Sales Price (blue, left) and Gross Rent (red, right) by Year',
                    xlabel='Year',
                    color="blue", 
                    marker="o",
                    ax=ax
                   )
    # Gross Rent right y axis subplot
    rent_plot = sfo_data['gross_rent'].groupby('year').mean()
    rent_plot.plot(color='red', 
                   marker='o',
                   ax=ax2)
    
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

def average_rent_by_neighborhood():
    sfo_grouped = sfo_data.groupby(['year', 'neighborhood']).mean().reset_index()
    fig = sfo_grouped.hvplot.line(x='year', 
                                  xlabel='Year',
                                  y='gross_rent',
                                  ylabel='Mean Gross Rent',
                                  groupby='neighborhood'
                                 )
    return hv.render(fig)

def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    fig = top_10.hvplot.bar(x='neighborhood',
                            xlabel='Neighborhood',
                            rot=37,
                            y='sale_price_sqr_foot',
                            ylabel='Mean Sale Price per Sq Ft,',
                            title='Top 10 Most Expensive San Francisco Neighborhoods, Avg 2010-2016',
                            frame_width=600,
                            frame_height=250
                           )
    return hv.render(fig)

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
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    top_10['gross_rent'] = top_10['gross_rent'].round(2)
    top_10['sale_price_sqr_foot'] = top_10['sale_price_sqr_foot'].round(2)
    fig = px.parallel_coordinates(top_10,
                                  title='Parallel Coordinates',
                                  dimensions=['sale_price_sqr_foot', 
                                              'housing_units', 
                                              'gross_rent'
                                             ],
                                  color='sale_price_sqr_foot',
                                  color_continuous_scale=px.colors.sequential.Inferno,
                                  labels={"sale_price_sqr_foot": "Sale Price per Sq Ft",
                                          "housing_units": "Housing Units",
                                          "gross_rent": 'Gross Rent'
                                         },
                                 )
    return fig

def parallel_categories():
    """Parallel Categories Plot."""
    top_10 = sfo_data.groupby('neighborhood').mean().nlargest(10, 'sale_price_sqr_foot').reset_index()
    top_10['gross_rent'] = top_10['gross_rent'].round(2)
    top_10['sale_price_sqr_foot'] = top_10['sale_price_sqr_foot'].round(2)
    fig = px.parallel_categories(top_10,
                                 title='Parallel Categories',
                                 dimensions=['neighborhood',
                                             'sale_price_sqr_foot',
                                             'housing_units',
                                             'gross_rent'
                                            ],
                                 color='sale_price_sqr_foot',
                                 color_continuous_scale=px.colors.sequential.Inferno,
                                 labels={"neighborhood": "Neighborhood",
                                         "sale_price_sqr_foot": "Sale Price per Sq Ft",
                                         "housing_units": "Housing Units",
                                         "gross_rent": 'Gross Rent'
                                        }
                                )
    return fig
                           
def neighborhood_map():
    """Neighborhood Map."""
    sfon = sfo_data.groupby('neighborhood').mean()
    sfo_location = pd.concat([neighborhood_data, sfon], axis=1)
    sfo_location = sfo_location.dropna()
    map_plot = px.scatter_mapbox(sfo_location,
                                 title='Mean Sale Price (marker size) and Gross Rent (marker color) in San Francisco 2010-2016',
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
    return map_plot

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

# Sidebar with selectbox to choose which plot to show
with st.sidebar:
    plot_choice = st.selectbox("Choose a plot:",
                               ("Housing Units per Year", 
                                'Average Gross Rent and Sale Price (seperate)',
                                "Average Gross Rent and Sale Price (together)",
                                "Average Price by Neighborhood",
                                "Average Rent by Neighborhood",
                                "Top 10 Expensive Neighborhoods",
                                "Top Expensive Neighborhoods Rent and Sales",
                                "Parallel Coordinates",
                                "Parallel Categories",
                                "Sunburst: Most expensive Neighborhoods 2010-2016",
                                "Neighborhood Map: Rent and Sale Prices 2010-2016"
                               )
                              )
    
if (plot_choice == 'Housing Units per Year'):
    st.pyplot(housing_units_per_year())
elif (plot_choice == "Average Gross Rent and Sale Price (seperate)"):
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(average_gross_rent())
    with col2:
        st.pyplot(average_sales_price())
elif (plot_choice == "Average Gross Rent and Sale Price (together)"):
    st.pyplot(average_rent_and_price())
elif (plot_choice == "Average Price by Neighborhood"):
    st.bokeh_chart(average_price_by_neighborhood())
elif (plot_choice == "Average Rent by Neighborhood"):
    st.bokeh_chart(average_rent_by_neighborhood())
elif (plot_choice == "Top 10 Expensive Neighborhoods"):
    st.bokeh_chart(top_most_expensive_neighborhoods())
elif (plot_choice == "Top Expensive Neighborhoods Rent and Sales"):
    st.bokeh_chart(most_expensive_neighborhoods_rent_sales())
elif (plot_choice == "Parallel Coordinates"):
    st.plotly_chart(parallel_coordinates())
elif (plot_choice == "Parallel Categories"):
    st.plotly_chart(parallel_categories())
elif (plot_choice == "Sunburst: Most expensive Neighborhoods 2010-2016"):
    st.plotly_chart(sunburst())
elif (plot_choice == "Neighborhood Map: Rent and Sale Prices 2010-2016"):
    st.plotly_chart(neighborhood_map())
    
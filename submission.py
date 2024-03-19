import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime as dt
import base64
import io
import os

# Load data
df = pd.read_csv('2.7_newyork_data_sample.csv', index_col=0)

# Groupby start stations
df['value'] = 1 
df_groupby_bar = df.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
top20 = df_groupby_bar.nlargest(20, 'value')

# Set page configuration
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon=":bike:"
)

# Define the aspect variable for different sections
selected_aspect = st.selectbox(
    "Select an aspect of the analysis:",
    ["Intro", "Exploring Weekly Bike Rides and Temperature Trends in New York City", "Top 20 Bike Stations in NYC (2022)", "Exploring Geographic Insights Through Interactive Map Screenshots", "Conclusions"],
    index=0
)

##### Intro Page #####
if selected_aspect == "Intro":
    # Add a title and descriptive text for the Intro page
    st.title("2022 Citi Bike Data Analysis: Enhancing New York City Distribution Strategy")
    st.write("""
    Welcome to the Citi Bike Distribution Analysis Dashboard. As lead analyst for New York City's premier bike-sharing service, our aim is to analyze Citi Bike facility data to uncover actionable insights. Our goal: address distribution challenges to ensure a seamless user experience and bolster our reputation as eco-friendly transportation leaders.

Context: Citi Bike's popularity surged post-Covid–19, posing distribution challenges. This dashboard aids in diagnosing issues and providing logistics recommendations.

Let's delve into the data and optimize our bike distribution strategy.
    """)

    
    
##### Weather component and bike usage #####
elif selected_aspect == "Exploring Weekly Bike Rides and Temperature Trends in New York City":
    # Load the new dataset 'newyork_data_weekly.csv' as 'df_weekly'
    df_weekly = pd.read_csv('newyork_data_weekly.csv')
    
    # Add a title and descriptive text for the Weather component and bike usage page
    st.title("Exploring Weekly Bike Rides and Temperature Trends in New York City")
    st.write("""
    This section examines the relationship between weekly bike rides and temperature trends in New York City. By visualizing these factors together, we aim to understand how weather impacts bike usage patterns and distribution strategies.

Key Factors:

Bike Rides: Reflects user demand and usage patterns.

Temperature: Influences user preferences and biking activity.
    """)

    # Create the dual-axis line chart
    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    fig_line.add_trace(
        go.Scatter(x=df_weekly['date'], y=df_weekly['bike_rides_weekly'], name='Weekly Bike Rides'),
        secondary_y=False
    )
    fig_line.add_trace(
        go.Scatter(x=df_weekly['date'], y=df_weekly['avgTemp'], name='Weekly Temperature'),
        secondary_y=True
    )
    
    # Customize the layout of the chart
    fig_line.update_layout(
        xaxis_title='Month',
        yaxis_title='Average Bike Ride Count',
        width=900,
        height=600,
        title="Weekly Bike Rides and Temperature Trends"
    )
    
    # Display the dual-axis line chart
    
    st.plotly_chart(fig_line)
    
    # Add a Markdown section for interpretation of the chart's contents
    st.write("""
    **Insights:**

- Bike rides and temperature rise in tandem from March to May, suggesting warmer weather drives business growth.

- Business remains strong throughout the summer months, even as temperatures begin to drop. However, this trend shifts in the fall.

**Recommendation:**

- Consider scaling back bike availability between November and April to align with reduced demand during colder months.
    """)
    
    ##### Most popular stations ####
elif selected_aspect == "Top 20 Bike Stations in NYC (2022)":
    # Add a title and descriptive text for the Most popular stations page
    st.title("Top 20 Bike Stations in New York City (2022)")
    st.write("""
    This bar chart showcases the most popular bike stations in New York City based on trip counts recorded in 2022. Understanding station popularity is crucial for optimizing our logistics model.
    """)

    # Create the bar chart
    fig = go.Figure(go.Bar(
        x=top20['start_station_name'],
        y=top20['value'],
        marker={'color': top20['value'], 'colorscale': 'Reds'}
    ))
    
    # Customize the layout of the chart
    fig.update_layout(
        xaxis_title='Start Stations',
        yaxis_title='Sum of Trips',
        width=900,
        height=600,
        xaxis_tickangle=-25
    )
    
    # Display the bar chart
    
    st.plotly_chart(fig)
    
    # Add a Markdown section for interpretation of the chart's contents
    st.subheader("Insights")
    st.write("""
    - Color intensity corresponds to trip counts, with darker colors indicating higher usage.
    
- For instance, West 21st Street and 6th Avenue recorded over 3000 trips, represented by deep red.

- In contrast, 9th Avenue and West 22nd Street show lighter shades, indicating lower trip numbers just over 2000.

- Majority of stations fall within the range of 2000 to 2500 trips, reflecting consistent usage patterns. While the top 25% exhibit exceptional trip numbers, they are not representative of typical trip volumes across most locations.

**Recommendation:**

- Consider implementing strategies to ensure bikes are always stocked at the most popular stations to meet user demand effectively.
    """)
    
##### Interactive map with aggregated bike trips ####
elif selected_aspect == "Exploring Geographic Insights Through Interactive Map Screenshots":
    # Add a title and descriptive text for the Most popular stations page
    st.title("Exploring Geographic Insights Through Interactive Map Screenshots")
    st.write("""
    This page presents five screenshots from our interactive map for detailed analysis. Leveraging geographical data allows us to establish direct correlations with locations, enhancing our understanding and insights.
    """)
    
    # Define image information with titles and descriptions
    image_info = {
        'kepler.gl.startpoint.png': ('Starting Point', 'Displays starting positions of various routes.'),
        'kepler.gl.startend.arc.png': ('Start to End | Arc', 'Illustrates routes with arcs connecting start and end points.'),
        'kepler.gl.endpoint.png': ('Ending Point', 'Shows ending positions of different routes.'),
        'kepler.gl.startend.line.png': ('Start to End | Line', 'Represents routes with lines connecting start and end points.'),
        'kepler.gl.tripsfilter.png': ('Trips', 'Highlights popular routes filtered through the Trips feature.'),
    }

     # Display images with titles and descriptions
    col1, col2 = st.columns(2)  # Split the page into two columns

    for index, (image_path, (title, description)) in enumerate(image_info.items()):
        # Read the image file as binary data
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Display the image along with its title and description
        if index < 2:
            with col1:
                st.image(image_bytes, caption=title, use_column_width=True, width=500)  # Adjust the width as needed
                st.write(description)
        else:
            with col2:
                st.image(image_bytes, caption=title, use_column_width=True, width=500)  # Adjust the width as needed
                st.write(description)

    # Add Insights section
    st.subheader("Insights")
    st.write("""
    - The 'Trips' image reveals top routes, aiding geographical analysis for understanding popularity.
    
- 'Starting Point' brightness indicates areas with higher rider density, suggesting increased demand and sales opportunities.

- 'Start to End | Arc' demonstrates routes leaving the downtown core, informing decisions on station placement for optimal coverage and sales potential.

**Recommendation:**

- Consider utilizing similar visualizations to determine the optimal number of stations to add along the waterfront.
    """)

        
##### Conclusions ####
elif selected_aspect == "Conclusions":
    # Add a title and descriptive text for the Conclusions page
    st.title("Key Insights from the Visualizations")
    
    # Seasonal Demand Trends
    st.write("""
    **Seasonal Demand Trends:**
    
    Bike trips peak in spring and summer, emphasizing seasonal demand patterns. Optimizing distribution strategies is crucial for meeting fluctuating demand effectively.
    """)
    
    # Station Usage Patterns
    st.write("""
    **Station Usage Patterns:**
    
    Most stations exhibit consistent usage, with some outliers like West 21st Street and 6th Avenue showing potential for increased bike availability.
    """)
    
    # Geographical Analysis for Expansion
    st.write("""
    **Geographical Analysis for Expansion:**
    
    Identifying popular routes and areas with high rider density informs expansion opportunities. Brighter map areas indicate higher demand, guiding bike allocation and potential sales growth.
    """)
    
    # Strategic Insights for Business Development
    st.write("""
    **Strategic Insights for Business Development:**
    
    Leverage visualizations like 'Start to End | Arc' to identify high-demand locations and plan distribution strategies accordingly.
    """)
    
    # Recommendations
    st.subheader("Recommendations")
    
    # Optimize Bike Distribution
    st.write("""
    **Optimize Bike Distribution:**

- Implement dynamic redistribution strategies based on real-time data analytics to ensure availability and prevent station overcrowding.

- Consider user incentives for returning bikes to less congested stations.
    """)
    
    # Expand Service Coverage
    st.write("""
    **Expand Service Coverage:**
    
- Focus on expanding service coverage in high-density areas and popular routes.

- Conduct market research for targeted expansion efforts to capture new user segments and increase ridership.
    """)


### Add the map  ###

# Path to your HTML file
path_to_html = "keplergl_map22.html"

# Read HTML file and store its content in a variable
with open(path_to_html, 'r') as f:
    html_data = f.read()

# Display HTML content on the Streamlit dashboard
st.header("Bike Trip Map of NYC")
st.components.v1.html(html_data, height=1000)

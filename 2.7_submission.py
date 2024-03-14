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
    ["Intro page", "Weather component and bike usage", "Most popular stations", "Interactive map with aggregated bike trips", "Conclusions"],
    index=0
)

##### Intro Page #####
if selected_aspect == "Intro page":
    # Add a title and descriptive text for the Intro page
    st.title("Analyzing Citi Bike Data for Improved Distribution Strategy in NYC")
    st.write("""
    Welcome to the Citi Bike Distribution Analysis Dashboard. As the lead analyst for a bike-sharing service based in New York City, our objective is to conduct a descriptive analysis of existing data from Citi Bike facilities. Our goal is to uncover actionable insights to address distribution issues, ensuring a seamless experience for our users and further solidifying our position as a leader in eco-friendly transportation solutions in the city.

    Context: Citi Bike has experienced increased popularity, particularly since the Covid–19 pandemic, leading to higher demand and distribution challenges. This dashboard serves as a tool to diagnose distribution issues and provide informed recommendations to enhance our logistics model.

    Let's explore the data and discover insights to optimize our bike distribution strategy.
    """)

    
    
##### Weather component and bike usage #####
elif selected_aspect == "Weather component and bike usage":
    # Load the new dataset 'newyork_data_weekly.csv' as 'df_weekly'
    df_weekly = pd.read_csv('newyork_data_weekly.csv')
    
    # Add a title and descriptive text for the Weather component and bike usage page
    st.title("Weather Component and Bike Usage Analysis")
    st.write("""
    This section focuses on analyzing the relationship between weekly bike rides and temperature trends in New York City. By visualizing these two key factors together, we aim to uncover insights into how weather conditions impact bike usage patterns, user behavior, and distribution strategies.
    
    Bike Rides: Weekly count of bike rides, reflecting user demand and usage patterns.
    
    Temperature: Weekly average temperature, influencing user preferences and biking activity.
    
    Understanding the correlation between these variables can help optimize distribution strategies, address availability issues, and enhance the overall biking experience for users across the city.
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
    
    The interactive chart above showcases the weekly trends of bike rides and temperature in New York City.
    
    - The rise of temperature, and bike rides, are virtually in lock step with one another in March, April and May. We can assume that the warmer weather will drive business growth moving into the summer months.
    
    - Business throughout the summer months is at it's strongest, but I also noticed that it continues to stay relatively strong despite temperatures beginning to drop. This is interesting, as we saw temperature and business grow identically in the spring, but that is not the case in the fall. 
    """)
    
    ##### Most popular stations ####
elif selected_aspect == "Most popular stations":
    # Add a title and descriptive text for the Most popular stations page
    st.title("Top 20 Most Popular Bike Stations in New York City")
    st.write("""
    This bar chart displays the top 20 most popular bike stations in New York City in 2022 based on the number of trips recorded. Understanding the popularity of these stations is essential for evaluating distribution patterns and identifying areas for improvement in our logistics model.
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
    st.subheader("Top 20 Most Popular Bike Stations in New York City")
    st.plotly_chart(fig)
    
    # Add a Markdown section for interpretation of the chart's contents
    st.subheader("Insights")
    st.write("""
    - The color intensity in the chart corresponds to the number of trips, with darker colors indicating higher trip counts. For instance, West 21st Street and 6th Avenue stand out with over 3000 trips, represented by a deep red color. In contrast, 9th Avenue and West 22nd Street show lighter shades, indicating lower trip numbers just over 2000.
    
    - The majority of stations in this graph fall within the range of 2000 to 2500 trips, highlighting consistent usage patterns. While the top 25% exhibit exceptional trip numbers, they do not represent the typical trip volumes observed across most locations.
    """)
    
##### Interactive map with aggregated bike trips ####
elif selected_aspect == "Interactive map with aggregated bike trips":
    # Add a title and descriptive text for the Most popular stations page
    st.title("Interactive map with aggregated bike trips")
    st.write("""
    On this page, we present five distinct screenshots extracted from our interactive map, meticulously selected for in-depth analysis. Leveraging a geographical perspective of our data confers a strategic advantage, enabling us to establish direct correlations with locations. The visual representation on a map transcends mere textual addresses, enhancing our understanding and insights.
    """)
    
    # Define image information with titles and descriptions
    image_info = {
        'kepler.gl.tripsfilter.png': ('Trips', 'In this image, we can see how the Trips filter is utilized to narrow down routes to a select few, revealing the most popular routes.'),
        'kepler.gl.startpoint.png': ('Starting Point', 'This image displays map points indicating the starting positions of various routes.'),
        'kepler.gl.endpoint.png': ('Ending Point', 'Here, we observe map points representing the ending positions of different routes.'),
        'kepler.gl.startend.arc.png': ('Start to End | Arc', 'Illustrating both the start and end points of a route with an arc connecting them.'),
        'kepler.gl.startend.line.png': ('Start to End | Line', 'Showing the start and end points of a route with a line connecting them.'),
    }

    # Display images with titles and descriptions
    for image_path, (title, description) in image_info.items():
        # Read the image file as binary data
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Display the image along with its title and description
        st.image(image_bytes, caption=title, use_column_width=True)
        st.write(description)

    # Add Insights section
    st.subheader("Insights")
    st.write("""
    - There are 3 main takeaways from these images. First, in the 'Trips' image, we can see clearly where our top 10 or so most popular routes are located. This allows us to understand why that might be as additional geographical analysis can be made around those addresses
    -  Secondly, the 'Starting Point' image gives us a clear idea of where we not only are covering in NYC but where it becomes brighter and more dense. This means certain areas have more riders, which means the need for more units, more opportunity, and ultimately, more sales.
    - Lastly, I'd like to direct your attention to the 'Start to End | Arc' image. We can see that in the center of the city, there is a large swath of rides that leave the downtown core and move outward. We can learn from this, and use similar visualizations on the map to determine our locations that require the greatest need, and as I mentioned in the last point, the most sales.
    """)
        
##### Conclusions ####
elif selected_aspect == "Conclusions":
    # Add a title and descriptive text for the Conclusions page
    st.title("Key Insights from the Visualizations")
    
    # Seasonal Demand Trends
    st.write("""
    Seasonal Demand Trends:
    
    Bike Trips show a significant increase during the spring and summer months compared to fall and winter, indicating strong seasonal demand patterns.
    Understanding these trends can help optimize bike distribution strategies to meet fluctuating demand effectively.
    """)
    
    # Station Usage Patterns
    st.write("""
    Station Usage Patterns:
    
    Most stations have trip numbers ranging from 2000 to 2500, showcasing consistent usage patterns across locations.
    Stations like West 21st Street and 6th Avenue stand out with higher trip volumes, suggesting potential areas for increased bike availability.
    """)
    
    # Geographical Analysis for Expansion
    st.write("""
    Geographical Analysis for Expansion:
    
    Identifying the top 10 popular routes and areas with higher rider density can guide geographical analysis for expansion opportunities.
    Brighter and denser areas on the map indicate higher demand, signaling the need for more bikes, improved coverage, and potential sales growth.
    """)
    
    # Strategic Insights for Business Development
    st.write("""
    Strategic Insights for Business Development:
    
    Utilize visualizations like the 'Start to End | Arc' image to pinpoint locations with high demand and plan distribution strategies accordingly.
    Focus on areas where rides move outward from the downtown core to optimize bike availability and capitalize on sales opportunities.
    """)
    
    # Recommendations
    st.subheader("Recommendations")
    
    # Optimize Bike Distribution
    st.write("""
    Optimize Bike Distribution:
    
    Implement dynamic bike redistribution strategies to address peak seasonal demand, especially during spring and summer months.
    Utilize real-time data analytics to identify high-demand locations and adjust bike allocation to ensure availability and prevent station overcrowding.
    Consider incentivizing users to return bikes to less congested stations through rewards or discounts to balance distribution across the network.
    """)
    
    # Expand Service Coverage
    st.write("""
    Expand Service Coverage:
    
    Focus on expanding service coverage in areas with high rider density and popular routes identified through geographical analysis.
    Establish new bike stations in strategic locations to meet growing demand, improve accessibility, and enhance customer satisfaction.
    Conduct market research to identify underserved neighborhoods or potential growth areas for targeted expansion efforts to capture new user segments and increase ridership.
    """)
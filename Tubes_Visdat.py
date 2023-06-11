import pandas as pd
from datetime import datetime
from bokeh.models import Slider, ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.formatters import DatetimeTickFormatter
import streamlit as st

# Load the COVID-19 dataset
data_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(data_url)
df = df[df['continent'] == 'Asia']

# Convert date column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Set the header/title
st.markdown("<h1 style='text-align: center; font-size: 24px;'>COVID-19 Cases in Asia</h1>", unsafe_allow_html=True)

# Create a figure for the line chart
p = figure(width=700, height=250, x_axis_type="datetime")

# Create a ColumnDataSource from the dataset
source = ColumnDataSource(df)

# Create a select widget for choosing the country
countries = df['location'].unique().tolist()
country_select = st.selectbox("Country", countries)

# Create a slider widget for selecting the date range
start_date = df['date'].min().to_pydatetime()
end_date = df['date'].max().to_pydatetime()
date_range = st.slider("Date Range", min_value=start_date, max_value=end_date, value=(start_date, end_date))

# Create a button to trigger data update
update_button = st.button("Update Data")

# Create a callback function for the button click event
def update_data():
    # Get the selected country and date range
    country = country_select
    start_date = date_range[0]
    end_date = date_range[1]
    
    # Filter the data based on the selected country and date range
    filtered_data = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Update the data source with the filtered data
    source.data = ColumnDataSource(filtered_data).data.copy()
    
# Handle button click event
if update_button:
    update_data()

# Plot the line chart
p.line(x='date', y='new_cases_smoothed', source=source, line_width=2)

# Format the x-axis tick labels to display dates in the desired format
p.xaxis.formatter = DatetimeTickFormatter(days="%d-%m-%Y")

# Display the plot
st.bokeh_chart(p)

import pandas as pd
from bokeh.models import Slider, ColumnDataSource, HoverTool, NumeralTickFormatter
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
p = figure(width=700, height=300, x_axis_type="datetime")

# Create a ColumnDataSource from the dataset
source = ColumnDataSource(df)

# Create a select widget for choosing the country
countries = df['location'].unique().tolist()
countries.insert(0, "All Countries")  # Add "All Countries" option
country_select = st.selectbox("Country", countries)

# Create a slider widget for selecting the date range
start_date = df['date'].min().to_pydatetime()
end_date = df['date'].max().to_pydatetime()
date_range = st.slider("Date Range", min_value=start_date, max_value=end_date, value=(start_date, end_date))

# Create a callback function for the button click event
def update_data():
    # Get the selected country and date range
    country = country_select
    start_date = date_range[0]
    end_date = date_range[1]
    
    if country == "All Countries":
        # Calculate total cases for all countries and date range
        filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        filtered_data = filtered_data.groupby('date')['new_cases_smoothed'].sum().reset_index()
        country = "All Countries"
    else:
        # Filter the data based on the selected country and date range
        filtered_data = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Update the data source with the filtered data
    source.data = ColumnDataSource(filtered_data).data.copy()
    
# Set initial data to show total cases for all countries
update_data()

# Plot the line chart
line = p.line(x='date', y='new_cases_smoothed', source=source, line_width=2)

# Add HoverTool to display values on hover
hover_tool = HoverTool(renderers=[line], tooltips=[("Date", "@date{%d-%m-%Y}"), ("New Cases", "@new_cases_smoothed{0,0}")],
                       formatters={'@date': 'datetime'}, mode='vline')
p.add_tools(hover_tool)

# Format the x-axis tick labels to display dates in the desired format
p.xaxis.formatter = DatetimeTickFormatter(days="%d-%m-%Y")

# Format the y-axis tick labels to display numbers without scientific notation
p.yaxis.formatter = NumeralTickFormatter(format="0,0")

# Display the plot
st.bokeh_chart(p)

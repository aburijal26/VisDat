import pandas as pd
from bokeh.io import curdoc, output_notebook,show
from bokeh.layouts import row, column
from bokeh.models import Select, DateRangeSlider, ColumnDataSource
from bokeh.plotting import figure

output_notebook()

# Load the COVID-19 dataset
data_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(data_url)

# Convert date column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Create a ColumnDataSource from the dataset
source = ColumnDataSource(df)

# Create a figure for the line chart
p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", title="COVID-19 Cases")
p.line(x='date', y='new_cases_smoothed', source=source, line_width=2)

# Create a callback function for the select and range slider
def update_data(attr, old, new):
    # Get the selected country and date range
    country = select.value
    start_date, end_date = date_range_slider.value_as_datetime
    
    # Filter the data based on the selected country and date range
    filtered_data = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Create a new ColumnDataSource from the filtered data
    new_source = ColumnDataSource(filtered_data)
    
    # Update the data source with the new filtered data
    source.data = new_source.data

# Create a select widget for choosing the country
countries = df['location'].unique().tolist()
select = Select(title="Country", options=countries, value=countries[0])
select.on_change('value', update_data)

# Create a date range slider widget for selecting the date range
start_date = df['date'].min()
end_date = df['date'].max()
date_range_slider = DateRangeSlider(title="Date Range", start=start_date, end=end_date, value=(start_date, end_date))
date_range_slider.on_change('value', update_data)

# Arrange the widgets and plot in a layout
layout = column(row(select, date_range_slider), p)

# Add the layout to the current document
curdoc().add_root(layout)

show(layout)

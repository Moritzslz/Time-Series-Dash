import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dotenv import load_dotenv

# Reading the sample data
df = pd.read_csv("sensor_readings.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

#print(df)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id="time-series-plot",
        config={'scrollZoom': True, 'displayModeBar': True}
    ),
    dcc.RangeSlider(
        id='date-range-slider',
        min=df['Timestamp'].min().timestamp(),
        max=df['Timestamp'].max().timestamp(),
        value=[df['Timestamp'].min().timestamp(), df['Timestamp'].max().timestamp()],
        marks={t.timestamp(): t.strftime('%Y-%m-%d') for t in pd.date_range(df['Timestamp'].min(), df['Timestamp'].max(), freq='1ME')}
    )
])


@app.callback(
    Output("time-series-plot", "figure"),
    [Input("date-range-slider", "value"),
     Input("time-series-plot", "relayoutData")]
)
def update_graph(date_range, relayout_data):
    start_date = pd.to_datetime(date_range[0], unit='s')
    end_date = pd.to_datetime(date_range[1], unit='s')

    filtered_df = df[(df["Timestamp"] >= start_date) & (df["Timestamp"] <= end_date)]

    # Debugging statement to check filtered data
    #print(f"Filtered Data: {filtered_df.head()}")
    print(f"Filtered Data Length: {len(filtered_df)}")

    # Check if there are any data points after filtering
    if filtered_df.empty:
        return {
            "data": [],
            "layout": go.Layout(
                title="Time Series Data",
                xaxis={"title": "Timestamp"},
                yaxis={"title": "SensorValue"},
                annotations=[{
                    "text": "No data available for the selected date range",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28}
                }]
            )
        }

    # Set the 'Timestamp' column as the index
    filtered_df.set_index("Timestamp", inplace=True)

    # Downsample the data to avoid performance issues
    zooming = relayout_data is not None and 'xaxis.range[0]' in relayout_data
    print(relayout_data)

    # If zooming or selecting, update the date range
    if zooming:
        start_date = pd.to_datetime(relayout_data['xaxis.range[0]'])
        end_date = pd.to_datetime(relayout_data['xaxis.range[1]'])

    # Determine the appropriate resampling frequency based on the selected time range
    time_range = end_date - start_date
    if time_range > pd.Timedelta(minutes=7):
        step = 1000
    elif time_range < pd.Timedelta(minutes=3):
        step = 100
    elif time_range < pd.Timedelta(minutes=1):
        step = 10
    else:
        step = 1

    downsampled_df = filtered_df.iloc[::step, :]

    # Debugging statement to check downsampled data
    #print(f"Downsampled Data: {downsampled_df.head()}")
    print(f"Downsampled Data Length: {len(downsampled_df)}")

    figure = {
        "data": [
            go.Scatter(
                x=downsampled_df.index,
                y=downsampled_df["SensorValue"],
                mode="lines",
                name="Value"
            )
        ],
        "layout": go.Layout(
            title="Time Series Data",
            xaxis={"title": "Timestamp"},
            yaxis={"title": "SensorValue"}
        )
    }
    return figure

if __name__ == "__main__":
    load_dotenv()
    port = int(os.environ.get("PORT", 8000))
    app.run_server(debug=False, port=port, host="0.0.0.0")

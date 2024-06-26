import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from dotenv import load_dotenv

# Reading the sample data
df = pd.read_csv("sensor_readings.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id="time-series-plot",
        config={'scrollZoom': True, 'displayModeBar': True}
    )
])

@app.callback(
    Output("time-series-plot", "figure"),
    [Input("time-series-plot", "relayoutData")]
)
def update_graph(relayout_data):
    if "xaxis.range[0]" in relayout_data:
        start_time = pd.to_datetime(relayout_data['xaxis.range[0]'])
        end_time = pd.to_datetime(relayout_data['xaxis.range[1]'])
    else:
        start_time = pd.to_datetime(df["Timestamp"].min())
        end_time = pd.to_datetime(df["Timestamp"].max())

    filtered_df = df[(df["Timestamp"] >= start_time) & (df["Timestamp"] <= end_time)]

    # Debugging statement to check filtered data
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

    step = calculate_step(start_time, end_time)

    downsampled_df = filtered_df.iloc[::step, :]

    # Debugging statement to check downsampled data
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


def calculate_step(start_time, end_time):
    time_range = end_time - start_time

    if time_range >= pd.Timedelta(minutes=7):
        step = 500  # Show data every 500 milliseconds
    elif time_range >= pd.Timedelta(minutes=5):
        step = 250  # Show data every 250 milliseconds
    elif time_range >= pd.Timedelta(minutes=3):
        step = 100  # Show data every 100 milliseconds
    elif time_range >= pd.Timedelta(minutes=1):
        step = 50  # Show data every 50 milliseconds
    elif time_range >= pd.Timedelta(seconds=30):
        step = 10  # Show data every 10 milliseconds
    else:
        step = 1  # Show data every 1 millisecond

    return step

if __name__ == "__main__":
    load_dotenv()
    port = int(os.environ.get("PORT", 8000))
    app.run_server(debug=False, port=port, host="0.0.0.0")

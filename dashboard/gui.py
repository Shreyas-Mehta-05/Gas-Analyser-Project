# Install Dash and Plotly libraries if not already installed
# pip install dash pandas plotly

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import random
import datetime
import pandas as pd

# Create a Dash app instance
app = Dash(__name__)

# Create lists to store timestamps and temperature data
timestamps = []
temperature_data = []

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': '#1E1E1E'}, children=[
    dcc.Graph(id='temperature-graph'),
    
    # Adding an Interval component to update the graph every 1 second
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Interval set to 1 second (1000 ms)
        n_intervals=0  # Starting at 0 intervals
    )
])

# Define the callback function to update the graph
@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_temperature_graph(n):
    # Generate dummy temperature data and append to the list
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_temp = random.uniform(20.0, 30.0)  # Random temperature value for demonstration
    
    timestamps.append(current_time)
    temperature_data.append(current_temp)
    
    # Keep the last 10 data points for real-time graph
    timestamps_trimmed = timestamps[-10:]
    temperature_data_trimmed = temperature_data[-10:]
    
    # Create the figure with real-time temperature data
    fig = {
        'data': [go.Scatter(
            x=timestamps_trimmed,
            y=temperature_data_trimmed,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#FF6F61', width=3)
        )],
        'layout': go.Layout(
            title='Real-Time Temperature',
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            font=dict(color='#FFFFFF'),
            xaxis=dict(title='Time', tickformat='%H:%M:%S', gridcolor='#333333'),
            yaxis=dict(title='Temperature (°C)', gridcolor='#333333'),
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

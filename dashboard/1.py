import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import plotly.graph_objs as go
from datetime import datetime

# MQTT Settings
broker = "172.20.10.4"
port = 1883
topic = "esp32/data"
buzzer_topic = "esp32/buzzer"
mqtt_username = "user3"
mqtt_password = "hello3"

buzzer = False

# Data storage for the graphs
temperature_data = []
humidity_data = []
co_data = []
rs_data = []
timestamps = []

# MQTT client setup
def on_message(client, userdata, message):
    global temperature_data, humidity_data, co_data, rs_data, timestamps
    try:
        decoded_message = message.payload.decode("utf-8")
        temp_str, hum_str, co_str, rs_str = decoded_message.split(",")

        # Convert to float
        temperature = float(temp_str)
        humidity = float(hum_str)
        co = float(co_str)
        rs = float(rs_str)

        # Append data
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        co_data.append(co)
        rs_data.append(rs)
        timestamps.append(datetime.now())

    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT client setup function
def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_start()
    return client

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "#1E1E1E", "color": "white", "padding": "20px"},
    children=[
        html.H1("Real-Time Sensor Data Dashboard", style={"textAlign": "center", "color": "#F2F2F2"}),

        html.Div([
            html.Div([
                html.H4("Temperature:", style={"color": "#FF6F61"}),
                html.P(id="temp-display", children="-- °C", style={"color": "#FFFFFF"})
            ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4("Humidity:", style={"color": "#61AFFF"}),
                html.P(id="hum-display", children="-- %", style={"color": "#FFFFFF"})
            ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4("CO:", style={"color": "#FFDD61"}),
                html.P(id="co-display", children="-- ppm", style={"color": "#FFFFFF"})
            ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4("Resistance:", style={"color": "#61FF87"}),
                html.P(id="rs-display", children="-- Ω", style={"color": "#FFFFFF"})
            ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'})
        ]),
        
        # let's add the gauge for CO here
        dcc.Graph(id="co-gauge"),
        html.Div([
            html.H4("CO Level", style={"color": "#FFDD61"}),
            html.P(id="co-level", children="--", style={"color": "#FFFFFF"})
        ], style={'textAlign': 'center'}),

        # lets add a temperature fancy scale here based on the current temperature value
        dcc.Graph(id="temp-scale"),
        html.Div([
            html.H4("Temperature Scale", style={"color": "#FF6F61"}),
            html.P(id="temp-scale-value", children="--", style={"color": "#FFFFFF"})
        ], style={'textAlign': 'center'}),






        dcc.Graph(id="temperature-graph"),
        dcc.Graph(id="humidity-graph"),
        dcc.Graph(id="rs-graph"),
        dcc.Graph(id="co-graph"),

        html.Div([
            html.Button('Toggle Buzzer', id='buzzer-button', n_clicks=0, 
                        style={'width': '20%', 'background-color': '#FF4136', 'color': 'white', 'padding': '10px'}),
        ], style={"textAlign": "center", "margin-top": "20px"}),

        dcc.Interval(id='interval-component', interval=2 * 1000, n_intervals=0)  # 2 seconds interval
    ]
)

# Update temperature graph
@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_temperature_graph(n):
    return {
        'data': [go.Scatter(x=timestamps[-10:], y=temperature_data[-10:], mode='lines+markers', name='Temperature', line=dict(color='#FF6F61', width=3))],
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

# Update humidity graph
@app.callback(
    Output('humidity-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_humidity_graph(n):
    return {
        'data': [go.Scatter(x=timestamps[-10:], y=humidity_data[-10:], mode='lines+markers', name='Humidity', line=dict(color='#61AFFF', width=3))],
        'layout': go.Layout(
            title='Real-Time Humidity',
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            font=dict(color='#FFFFFF'),
            xaxis=dict(title='Time', tickformat='%H:%M:%S', gridcolor='#333333'),
            yaxis=dict(title='Humidity (%)', gridcolor='#333333'),
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }

# Update resistance graph
@app.callback(
    Output('rs-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_rs_graph(n):
    return {
        'data': [go.Scatter(x=timestamps[-10:], y=rs_data[-10:], mode='lines+markers', name='Rs', line=dict(color='#61FF87', width=3))],
        'layout': go.Layout(
            title='Real-Time Rs',
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            font=dict(color='#FFFFFF'),
            xaxis=dict(title='Time', tickformat='%H:%M:%S', gridcolor='#333333'),
            yaxis=dict(title='Rs (Ω)', gridcolor='#333333'),
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }

# Update CO graph
@app.callback(
    Output('co-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_co_graph(n):
    return {
        'data': [go.Scatter(x=timestamps[-10:], y=co_data[-10:], mode='lines+markers', name='CO', line=dict(color='#FFDD61', width=3))],
        'layout': go.Layout(
            title='Real-Time CO',
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            font=dict(color='#FFFFFF'),
            xaxis=dict(title='Time', tickformat='%H:%M:%S', gridcolor='#333333'),
            yaxis=dict(title='CO (ppm)', gridcolor='#333333'),
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }

# update the CO gauge
@app.callback(
    Output('co-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_co_gauge(n):
    if co_data:
        co_value = co_data[-1]
    else:
        co_value = 0
    
    return {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=co_value,
                title={'text': "CO (ppm)"},
                gauge={'axis': {'range': [0, 1000]},
                       'bar': {'color': "#FFDD61"},
                       'steps': [
                           {'range': [0, 500], 'color': "#FFC371"},
                           {'range': [500, 1000], 'color': "#FF6347"}],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 900}},
            )
        ],
        'layout': go.Layout(
            paper_bgcolor='#1E1E1E',
            font={'color': 'white'}
        )
    }


# update the temperature scale
@app.callback(
    Output('temp-scale', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_temp_scale(n):
    if temperature_data:
        temp_value = temperature_data[-1]
    else:
        temp_value = 0
    
    return {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=temp_value,
                title={'text': "Temperature (°C)"},
                gauge={'axis': {'range': [0, 50]},
                       'bar': {'color': "#FF6F61"},
                       'steps': [
                           {'range': [0, 10], 'color': "#FF6347"},
                           {'range': [10, 20], 'color': "#FF7F50"},
                           {'range': [20, 30], 'color': "#FFA07A"},
                           {'range': [30, 40], 'color': "#FFC371"},
                           {'range': [40, 50], 'color': "#FFD700"}],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}},
            )
        ],
        'layout': go.Layout(
            paper_bgcolor='#1E1E1E',
            font={'color': 'white'}
        )
    }

# Rest of the code remains the same for updating displays and buzzer


# Main function to run the app
if __name__ == '__main__':
    # Set up MQTT client
    mqtt_client = setup_mqtt()
    # Run Dash app
    app.run_server(debug=True)

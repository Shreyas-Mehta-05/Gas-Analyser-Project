import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import plotly.graph_objs as go
from datetime import datetime
import dash_leaflet as dl

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
        # html.H1("Real-Time Sensor Data Dashboard", style={"textAlign": "center", "color": "#F2F2F2"}),

        # html.Div([
        #     html.Div([
        #         html.H4("Temperature:", style={"color": "#FF6F61"}),
        #         html.P(id="temp-display", children="-- °C", style={"color": "#FFFFFF"})
        #     ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

        #     html.Div([
        #         html.H4("Humidity:", style={"color": "#61AFFF"}),
        #         html.P(id="hum-display", children="-- %", style={"color": "#FFFFFF"})
        #     ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

        #     html.Div([
        #         html.H4("CO:", style={"color": "#FFDD61"}),
        #         html.P(id="co-display", children="-- ppm", style={"color": "#FFFFFF"})
        #     ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'}),

        #     html.Div([
        #         html.H4("Resistance:", style={"color": "#61FF87"}),
        #         html.P(id="rs-display", children="-- Ω", style={"color": "#FFFFFF"})
        #     ], style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'})
        # ]),
       html.H1("Real-Time Sensor Data Dashboard", 
        style={
            "textAlign": "center",
            "color": "#F2F2F2",  # Fallback for unsupported browsers
            "background": "linear-gradient(90deg, #FF6F61, #61AFFF)",
            "-webkit-background-clip": "text",
            "color": "transparent",  # Ensures gradient is shown as text color
            "font-family": "'Roboto', sans-serif",  # Modern font
            "padding-bottom": "20px",
            "font-weight": "bold",
            "font-size": "48px",  # Larger text for impact
            "text-shadow": "2px 2px 10px rgba(0, 0, 0, 0.5)",  # Cool shadow effect
            "letter-spacing": "1px"  # Slight letter spacing for modern feel
        }),

    html.Div([
    # Temperature Display
    html.Div([
        html.H4("Temperature:", style={"color": "#1E1E1E", "font-weight": "bold", "padding-top": "5px", "font-size": "18px"}),  # Increased font size
        html.P(id="temp-display", children="-- °C", style={"color": "#1E1E1E", "font-size": "22px", "font-weight": "bold"})  # Increased font size
    ], style={
        'width': '20%', 'display': 'inline-block', 'textAlign': 'center',
        'background-color': '#FF6F61', 'padding': '10px', 'border-radius': '8px', 
        'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)', 'margin': '5px'
    }),

    # Humidity Display
    html.Div([
        html.H4("Humidity:", style={"color": "#1E1E1E", "font-weight": "bold", "padding-top": "5px", "font-size": "18px"}),  # Increased font size
        html.P(id="hum-display", children="-- %", style={"color": "#1E1E1E", "font-size": "22px", "font-weight": "bold"})  # Increased font size
    ], style={
        'width': '20%', 'display': 'inline-block', 'textAlign': 'center',
        'background-color': '#61AFFF', 'padding': '10px', 'border-radius': '8px', 
        'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)', 'margin': '5px'
    }),

    # CO Display
    html.Div([
        html.H4("CO:", style={"color": "#1E1E1E", "font-weight": "bold", "padding-top": "5px", "font-size": "18px"}),  # Increased font size
        html.P(id="co-display", children="-- ppm", style={"color": "#1E1E1E", "font-size": "22px", "font-weight": "bold"})  # Increased font size
    ], style={
        'width': '20%', 'display': 'inline-block', 'textAlign': 'center',
        'background-color': '#FFDD61', 'padding': '10px', 'border-radius': '8px', 
        'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)', 'margin': '5px'
    }),

    # Resistance Display
    html.Div([
        html.H4("Resistance:", style={"color": "#1E1E1E", "font-weight": "bold", "padding-top": "5px", "font-size": "18px"}),  # Increased font size
        html.P(id="rs-display", children="-- Ω", style={"color": "#1E1E1E", "font-size": "22px", "font-weight": "bold"})  # Increased font size
    ], style={
        'width': '20%', 'display': 'inline-block', 'textAlign': 'center',
        'background-color': '#61FF87', 'padding': '10px', 'border-radius': '8px', 
        'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)', 'margin': '5px'
    })
], style={'textAlign': 'center', 'padding': '10px'}),

    

       html.Div([
        # A container for all gauges in one row
        html.Div([
            # CO Gauge (unchanged)
            html.Div([
                dcc.Graph(
                    id="co-gauge",
                    # config={
                    #     'displayModeBar': False  # Hide toolbar for a cleaner look
                    # },
                    style={
                        'display': 'inline-block',
                        'width': '100%',
                        'height': '300px',
                        'padding': '10px',
                    }
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'left','backgroundColor': '#FFDD61','color':'black'}),  # Yellow colors, light yellow background

            # Humidity Gauge (Cool Theme)
            html.Div([
                dcc.Graph(
                    id="humidity-gauge",
                    config={
                        'displayModeBar': False  # Hide toolbar for a cleaner look
                    },
                    style={
                        'display': 'inline-block',
                        'width': '100%',
                        'height': '300px',
                        'padding': '10px',
                    }
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center', 'backgroundColor': '#ADD8E6'}),  # Cool colors, light blue background

            # Temperature Gauge (Hot Theme)
            html.Div([
                dcc.Graph(
                    id="temperature-gauge",
                    config={
                        'displayModeBar': False  # Hide toolbar for a cleaner look
                    },
                    style={
                        'display': 'inline-block',
                        'width': '100%',
                        'height': '300px',
                        'padding': '10px',
                    }
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'right', 'backgroundColor': '#FF6347'}),  # Hot colors, tomato background
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '80%', 'margin': '0 auto'})  # Flexbox for inline alignment and centering
    ]),


        

        # 2x2 Graph layout
        html.Div([
            html.Div([dcc.Graph(id="temperature-graph")], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
            html.Div([dcc.Graph(id="humidity-graph")], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
        ], style={'textAlign': 'center'}),
        html.Div([
            html.Div([dcc.Graph(id="rs-graph")], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
            html.Div([dcc.Graph(id="co-graph")], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
        ], style={'textAlign': 'center'}),

        html.Div([
            html.Button('Toggle Buzzer', 
                        id='buzzer-button', 
                        n_clicks=0, 
                        style={
                            'width': '25%',  # Slightly wider button
                            'background-color': '#FF4136',  # Red background
                            'color': 'white',  # White text color
                            'padding': '15px 20px',  # More padding: 15px for top/bottom, 20px for left/right
                            'font-size': '16px',  # Larger font size for better readability
                            'border': 'none',  # Remove border
                            'border-radius': '10px',  # Rounded corners for modern look
                            'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.2)',  # Shadow effect for a lifted look
                            'cursor': 'pointer',  # Pointer cursor on hover
                            'transition': 'background-color 0.3s ease',  # Smooth transition on hover
                        }
            ),
        ], style={"textAlign": "center", "margin-top": "20px"}),

        html.Div([
        html.H2("Deployment Map", 
                style={"textAlign": "center", "color": "#F2F2F2", "padding-bottom": "10px"}),
        dl.Map(id='map',  # Assigning an ID to the map for JS reference
               children=[
                   dl.TileLayer(),
                   dl.Marker(position=[17.3850, 78.4867], children=[
                       dl.Tooltip("Sensor Location"),
                       dl.Popup("Sensor 1: Details about the sensor")
                   ])
               ], 
               style={'width': '100%', 'height': '400px'}, 
               center=[17.3850, 78.4867], 
               zoom=12),
    ], style={
        'margin': '20px',  # Add margin around the map
        'padding': '10px',  # Add padding inside the map container
        'border-radius': '10px',  # Rounded corners
        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.3)',  # Shadow effect
        'background-color': '#1E1E1E'  # Background color for the map container
    }),
    
    html.Script("""
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                
                // Access the Leaflet map component
                const map = document.getElementById('map').leafletMap;  // Get the map reference
                
                // Set the view to the user's location
                map.setView([latitude, longitude], 12);
                
                // Add a marker for the user's location
                L.marker([latitude, longitude]).addTo(map).bindPopup("You are here").openPopup();
            }, function(error) {
                console.error("Error getting location: ", error.message);
            });
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    """),

        dcc.Interval(id='interval-component', interval=2 * 1000, n_intervals=0)  # 2 seconds interval
    ]
)

# Update temperature linear gauge display
@app.callback(
    Output('temperature-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_temperature_gauge(n):
    temperature_value = float(temperature_data) if temperature_data else 0
    return {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=temperature_value,
                gauge={
                    'axis': {'range': [0, 50]},
                    'bar': {'color': "#00FF00"},  # Color of the gauge needle
                    'steps': [
                        # {'range': [0, 10], 'color': "#FFC371"},  # Green for low temperature
                        # {'range': [10, 30], 'color': "#FF6347"},  # Yellow for medium temperature
                        # {'range': [30, 50], 'color': "#FF0000"}  # Red for high temperature
                        {
    'range': [0, 10], 'color': "#4B6EAF"},  # Cool Blue for low temperature
    {'range': [10, 20], 'color': "#A1C6E7"},  # Light Blue for mid-low temperatures
    {'range': [20, 30], 'color': "#F7C94C"},  # Warm Yellow for moderate temperatures
    {'range': [30, 40], 'color': "#F48C28"},  # Light Orange for mid-high temperatures
    {'range': [40, 50], 'color': "#E63946"}  # Vibrant Red for high temperatures
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': temperature_value
                    }
                },
                title={'text': "Temperature (°C)", 'font': {'color': 'white'}},
                number={'font': {'color': 'white'}}
            )
        ],
        'layout': go.Layout(
            paper_bgcolor='#1E1E1E',
            font=dict(color='white'),
            height=300,  # Resize the gauge
            width=300    # Resize the gauge
        )
    }

# update Humidity gauge
@app.callback(
    Output('humidity-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_humidity_gauge(n):
    humidity_value = float(humidity_data) if humidity_data else 0
    return {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=humidity_value,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#00FF00"},  # Color of the gauge needle
                    'steps': [
                        # {'range': [0, 30], 'color': "#FFC371"},  # Green for low humidity
                        # {'range': [30, 70], 'color': "#FF6347"},  # Yellow for medium relative humidity
                        # {'range': [70, 100], 'color': "#FF0000"}  # Red for high relative humidity
                         {'range': [0, 30], 'color': "#FF0000"},    # Bright Red
    {'range': [30, 60], 'color': "#FFB300"},   # Light Orange
    {'range': [60, 80], 'color': "#FFD54F"},   # Light Yellow
    {'range': [80, 90], 'color': "#AEEEEE"},    # Light Blue
    {'range': [90, 100], 'color': "#007FFF"}   



                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': humidity_value
                    }
                },
                title={'text': "Humidity (%)", 'font': {'color': 'white'}},
                number={'font': {'color': 'white'}}
            )
        ],
        'layout': go.Layout(
            paper_bgcolor='#1E1E1E',
            font=dict(color='white'),
            height=300,  # Resize the gauge
            width=300    # Resize the gauge
        )
    }



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

# Update CO gauge
@app.callback(
    Output('co-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_co_gauge(n):
    co_value = float(co_data) if co_data else 0
    return {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=co_value,
                gauge={
                    'axis': {'range': [0, 1000]},
                    'bar': {'color': "#00FF00"},  # Color of the gauge needle
                    'steps': [
                        {'range': [0, 500], 'color': "#FFC371"},  # Green for low CO levels
                        {'range': [500, 750], 'color': "#FF6347"},  # Yellow for medium levels
                        {'range': [750, 1000], 'color': "#FF0000"}  # Red for high levels
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': co_value
                    }
                },
                title={'text': "CO Concentration (ppm)", 'font': {'color': 'white'}},
                number={'font': {'color': 'white'}}
            )
        ],
        'layout': go.Layout(
            paper_bgcolor='#1E1E1E',
            font=dict(color='white'),
            height=300,  # Resize the gauge
            width=300    # Resize the gauge
        )
    }

# Toggle buzzer
@app.callback(
    Output('buzzer-button', 'children'),
    [Input('buzzer-button', 'n_clicks')]
)
def toggle_buzzer(n_clicks):
    if n_clicks > 0:
        mqtt_client.publish(buzzer_topic, "1")
    return  "Emergency Alert!"

# Start the MQTT client and run the Dash app
# client = setup_mqtt()

if __name__ == '__main__':
    app.run_server(debug=True)

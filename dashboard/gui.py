import tkinter as tk
from tkinter import Button, Scale, HORIZONTAL, Label
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime

# Use Matplotlib dark theme
plt.style.use('dark_background')

# MQTT Settings
broker = "172.20.10.4"
port = 1883
topic = "esp32/data"
buzzer_topic = "esp32/buzzer"
mqtt_username = "user3"
mqtt_password = "hello3"


# buzzer = False

# Data storage for the graphs
temperature_data = []
humidity_data = []
co_data = []
rs_data = []
timestamps = []  # To store the time of each data point

# Boolean flag for pausing and resuming the plotting
is_paused = False
view_index = 0  # Index to control which part of data to display

# Function to handle incoming MQTT messages
def on_message(client, userdata, message):
    global is_paused, view_index, canvas
    if not is_paused:
        try:
            # Decode message (assuming "temp,humidity,co,rs" format)
            decoded_message = message.payload.decode("utf-8")
            temp_str, hum_str, co_str, rs_str = decoded_message.split(",")
            
            # Convert the received strings to float
            temperature = float(temp_str)
            humidity = float(hum_str)
            co = float(co_str)
            rs = float(rs_str)

            # print(co)

            # Append new data to the lists
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            co_data.append(co)
            rs_data.append(rs)
            timestamps.append(datetime.now())  # Add current timestamp
            
            # Update each graph (show only 10 readings at a time)
            view_index = max(0, len(temperature_data) - 10)  # Start viewing from the latest 10 readings
            update_graphs()

            # Redraw the canvas with updated graphs
            canvas.draw()

            # Update the display labels with current sensor data
            temp_label.config(text=f"Temperature: {temperature:.2f} °C")
            humidity_label.config(text=f"Humidity: {humidity:.2f} %")
            co_label.config(text=f"CO: {co:.2f} ppm")
            rs_label.config(text=f"Resistance: {rs:.2f} Ω")

        except Exception as e:
            print(f"Error processing message: {e}")

# Function to update the graphs with only the visible data (10 readings)
def update_graphs():
    global canvas, scale
    ax1.clear()
    # we need a goo
    ax1.plot(timestamps[view_index:], temperature_data[view_index:], color='FF6500', label='Temperature')
    ax1.set_title("Real-Time Temperature", color='white')
    ax1.set_ylabel("Temperature (°C)", color='white')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.legend()
    ax1.grid(True, color='gray')

    ax2.clear()
    ax2.plot(timestamps[view_index:], humidity_data[view_index:], color='blue', label='Humidity')
    ax2.set_title("Real-Time Humidity", color='white')
    ax2.set_ylabel("Humidity (%)", color='white')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax2.legend()
    ax2.grid(True, color='gray')

    ax3.clear()
    ax3.plot(timestamps[view_index:], rs_data[view_index:], color='green', label='Rs')
    ax3.set_title("Real-Time Rs", color='white')
    ax3.set_ylabel("Rs (Ω)", color='white')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax3.legend()
    ax3.grid(True, color='gray')

    ax4.clear()
    ax4.plot(timestamps[view_index:], co_data[view_index:], color='orange', label='CO')
    ax4.set_title("Real-Time CO", color='white')
    ax4.set_ylabel("CO (%)", color='white')
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax4.legend()
    ax4.grid(True, color='gray')

    # Update the slider range to fit the data length
    scale.config(to=max(0, len(temperature_data) - 1))

# Function to control slider for adjusting the view of the graph
def adjust_view(val):
    global view_index
    view_index = int(val)
    update_graphs()
    canvas.draw()

# Function to display value when hovering over a point
# def on_hover(event):
#     global canvas
#     for i, (x, y) in enumerate(zip(timestamps[view_index:], temperature_data[view_index:])):
#         if event.inaxes == ax1:
#             # Check if the mouse is near a point on the graph
#             if abs(mdates.num2date(event.xdata) - x).total_seconds() < 1:
#                 ax1.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='white')
#                 canvas.draw()

# Function to setup MQTT client
def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_start()
    return client

# Function to control the buzzer via MQTT
def handle_buzzer():
    global buzzer
    mqtt_client.publish(buzzer_topic, "1")
    buzzer = True
    print("Buzzer ON message sent")

# Function to set up the Tkinter GUI
def setup_gui():
    global ax1, ax2, ax3, ax4, canvas  # Make them accessible globally

    root = tk.Tk()
    root.title("Real-Time Sensor Data Plot")
    root.config(bg="#2e2e2e")  # Set background to dark

    # Create labels to display current sensor data
    global temp_label, humidity_label, co_label, rs_label

    # Set dark theme for labels
    label_style = {"fg": "black", "font": ("Arial", 12), "width": 20}

    # Use grid to position the labels in a single row
    temp_label = tk.Label(root, text="Temperature: -- °C", **label_style,bg="#FF6500")
    temp_label.grid(row=0, column=0, padx=5, pady=5)

    humidity_label = tk.Label(root, text="Humidity: -- %", **label_style,bg="blue")
    humidity_label.grid(row=0, column=1, padx=5, pady=5)

    co_label = tk.Label(root, text="CO: -- ppm", **label_style,bg="yellow")
    co_label.grid(row=0, column=2, padx=5, pady=5)

    rs_label = tk.Label(root, text="Resistance: -- Ω", **label_style,bg="green")
    rs_label.grid(row=0, column=3, padx=5, pady=5)

    # Set up Matplotlib figure and four subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

    # Embed Matplotlib graphs in Tkinter window
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    
    # Place the canvas for the graphs in row 1 (below the labels)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

    # Create slider to scroll through the graph data
    global scale
    scale = Scale(root, from_=0, to=40, orient=HORIZONTAL, command=adjust_view, label="View Data",
                  bg="#2e2e2e", fg="white", troughcolor="#4c4c4c", highlightbackground="#2e2e2e")
    
    # Place the slider in row 2 (below the graphs)
    scale.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Button to control the buzzer
    buzzerButton = Button(root, text="Emergency", command=handle_buzzer, bg="red", fg="white", width=20)
    
    # Place the buzzer button in row 3 (below the slider)
    buzzerButton.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    # Configure row/column weights for resizing behavior
    root.grid_rowconfigure(1, weight=1)  # Allow row 1 (graphs) to expand
    root.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Allow columns to expand

    # Bind hover event for data point display
    # fig.canvas.mpl_connect("motion_notify_event", on_hover)

    return root

# MQTT client
mqtt_client = setup_mqtt()

# Setup and start the Tkinter GUI
root = setup_gui()
root.mainloop()

# Disconnect MQTT client when the program ends
mqtt_client.loop_stop()
mqtt_client.disconnect()
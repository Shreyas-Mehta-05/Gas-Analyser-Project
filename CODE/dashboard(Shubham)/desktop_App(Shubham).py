import tkinter as tk
from tkinter import Button, Scale, HORIZONTAL, Label
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime


plt.style.use('ggplot')
# use dark_background for dark mode
# plt.style.use('dark_background')
# Customize color palette
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9']
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
# def update_graphs():
#     global canvas, scale
#     ax1.clear()
#     ax1.plot(timestamps[view_index:], temperature_data[view_index:], color=colors[0], label='Temperature')
#     ax1.set_title("Real-Time Temperature")
#     ax1.set_ylabel("Temperature (°C)")
#     # also set the moving average and shadung
#     ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#     ax1.legend()
#     ax1.grid(True)

#     ax2.clear()
#     ax2.plot(timestamps[view_index:], humidity_data[view_index:], color=colors[1], label='Humidity')
#     ax2.set_title("Real-Time Humidity")
#     ax2.set_ylabel("Humidity (%)")
#     ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#     ax2.legend()
#     ax2.grid(True)

#     ax3.clear()
#     ax3.plot(timestamps[view_index:], rs_data[view_index:], color=colors[2], label='Rs')
#     ax3.set_title("Real-Time Rs")
#     ax3.set_ylabel("Rs (Ω)")
#     ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#     ax3.legend()
#     ax3.grid(True)

#     ax4.clear()
#     ax4.plot(timestamps[view_index:], co_data[view_index:], color=colors[3], label='CO')
#     ax4.set_title("Real-Time CO")
#     ax4.set_ylabel("CO (%)")
#     ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#     ax4.legend()
#     ax4.grid(True)

#     # Update the slider range to fit the data length
#     scale.config(to=max(0, len(temperature_data) - 1))


import numpy as np
import matplotlib.dates as mdates

# Define a function to calculate moving average
def moving_average(data, window_size):
    if len(data) < window_size:
        return np.array(data)  # Return as array even if it's too short
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def update_graphs():
    global canvas, scale
    ax1.clear()
    ax1.plot(timestamps[view_index:], temperature_data[view_index:], color=colors[0], label='Temperature')

    # Calculate and plot the moving average for temperature
    temp_moving_avg = moving_average(temperature_data[view_index:], window_size=5)
    temp_moving_avg_array = np.array(temp_moving_avg)  # Ensure it's a NumPy array
    start_index = len(temperature_data) - len(temp_moving_avg)  # Calculate start index for timestamps
    ax1.fill_between(timestamps[view_index:][start_index:], 
                     temp_moving_avg_array - 5, 
                     temp_moving_avg_array + 5, 
                     color='orange', alpha=0.1, label='±5°C Range')
    
    ax1.set_title("Real-Time Temperature")
    ax1.set_ylabel("Temperature (°C)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.legend()
    ax1.grid(True)

    ax2.clear()
    ax2.plot(timestamps[view_index:], humidity_data[view_index:], color=colors[1], label='Humidity')

    # Calculate and plot the moving average for humidity
    humidity_moving_avg = moving_average(humidity_data[view_index:], window_size=5)
    humidity_moving_avg_array = np.array(humidity_moving_avg)
    start_index = len(humidity_data) - len(humidity_moving_avg)
    ax2.fill_between(timestamps[view_index:][start_index:], 
                     humidity_moving_avg_array - 5, 
                     humidity_moving_avg_array + 5, 
                     color='lightblue', alpha=0.1, label='±5% Range')
    
    ax2.set_title("Real-Time Humidity")
    ax2.set_ylabel("Humidity (%)")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax2.legend()
    ax2.grid(True)

    ax3.clear()
    ax3.plot(timestamps[view_index:], rs_data[view_index:], color=colors[2], label='Rs')

    # Calculate and plot the moving average for Rs
    rs_moving_avg = moving_average(rs_data[view_index:], window_size=5)
    rs_moving_avg_array = np.array(rs_moving_avg)
    start_index = len(rs_data) - len(rs_moving_avg)
    ax3.fill_between(timestamps[view_index:][start_index:], 
                     rs_moving_avg_array - 5, 
                     rs_moving_avg_array + 5, 
                     color='lightgreen', alpha=0.1, label='±5Ω Range')
    
    ax3.set_title("Real-Time Rs")
    ax3.set_ylabel("Rs (Ω)")
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax3.legend()
    ax3.grid(True)

    ax4.clear()
    ax4.plot(timestamps[view_index:], co_data[view_index:], color=colors[3], label='CO')

    # Calculate and plot the moving average for CO
    co_moving_avg = moving_average(co_data[view_index:], window_size=5)
    co_moving_avg_array = np.array(co_moving_avg)
    start_index = len(co_data) - len(co_moving_avg)
    ax4.fill_between(timestamps[view_index:][start_index:], 
                     co_moving_avg_array - 0.5,  # Adjust range as needed
                     co_moving_avg_array + 0.5, 
                     color='pink', alpha=0.1, label='±0.5% Range')
    
    ax4.set_title("Real-Time CO")
    ax4.set_ylabel("CO (%)")
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax4.legend()
    ax4.grid(True)

    # Update the slider range to fit the data length
    scale.config(to=max(0, len(temperature_data) - 1))

    # Redraw the canvas
    # canvas.draw()





# Function to control slider for adjusting the view of the graph
def adjust_view(val):
    global view_index
    view_index = int(val)
    update_graphs()
    canvas.draw()

# Function to display value when hovering over a point
def on_hover(event):
    global canvas
    for i, (x, y) in enumerate(zip(timestamps[view_index:], temperature_data[view_index:])):
        if event.inaxes == ax1:
            # Check if the mouse is near a point on the graph
            if abs(mdates.num2date(event.xdata) - x).total_seconds() < 1:
                ax1.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
                canvas.draw()

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
    if buzzer == False:
        mqtt_client.publish(buzzer_topic, "1")
        buzzer = True
        print("Buzzer ON message sent")
    elif buzzer == True:
        mqtt_client.publish(buzzer_topic, "0")
        buzzer = False
        print("Buzzer OFF message sent")

# Function to set up the Tkinter GUI
def setup_gui():
    root = tk.Tk()
    root.title("Real-Time Sensor Data Plot")

    # Create labels to display current sensor data
    global temp_label, humidity_label, co_label, rs_label
    # Set the color palette for labels
    label_bg_color = "#f8f9fa"  # Light background
    label_fg_color = "#343a40"  # Dark text
    label_font = ("Helvetica", 14, "bold")  # Larger, bold font

    # Create labels to display current sensor data with enhanced appearance
    temp_label = tk.Label(root, text="Temperature: -- °C", font=label_font, width=20, bg=label_bg_color, fg=label_fg_color, relief="raised", borderwidth=2, padx=10, pady=10)
    temp_label.grid(row=0, column=0, padx=10, pady=10)

    humidity_label = tk.Label(root, text="Humidity: -- %", font=label_font, width=20, bg=label_bg_color, fg=label_fg_color, relief="raised", borderwidth=2, padx=10, pady=10)
    humidity_label.grid(row=0, column=1, padx=10, pady=10)

    co_label = tk.Label(root, text="CO: -- ppm", font=label_font, width=20, bg=label_bg_color, fg=label_fg_color, relief="raised", borderwidth=2, padx=10, pady=10)
    co_label.grid(row=0, column=2, padx=10, pady=10)

    rs_label = tk.Label(root, text="Resistance: -- Ω", font=label_font, width=20, bg=label_bg_color, fg=label_fg_color, relief="raised", borderwidth=2, padx=10, pady=10)
    rs_label.grid(row=0, column=3, padx=10, pady=10)

    # Set up Matplotlib figure and four subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

    # Embed Matplotlib graphs in Tkinter window
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    
    # Place the canvas for the graphs in row 1 (below the labels)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

    # Create a slider to scroll through the graph data
    global scale
    scale = Scale(
        root, 
        from_=0, 
        to=40, 
        orient=HORIZONTAL, 
        command=adjust_view, 
        label="View Data", 
        bg="#f0f0f0",            # Light background for the slider
        fg="black",               # Black text for better readability
        troughcolor="#b3cde0",    # Softer color for the trough
        activebackground="#6497b1", # Highlight color when interacting with the slider
        length=300,               # Set a larger width for the slider
        font=("Helvetica", 12, "bold")  # Bold font for the label
    )

    # Place the slider in row 2 (below the graphs)
    scale.grid(
        row=2, 
        column=0, 
        columnspan=4, 
        padx=10,  # Increase padding for better spacing
        pady=10, 
        sticky="ew"  # Make the slider stretch horizontally across the row
    )


    buzzerButton = Button(
        root, 
        text="Emergency",   # Add emojis to make the button more eye-catching
        command=handle_buzzer, 
        bg="#ff4d4d",            # Use a nicer shade of red
        fg="white",              # White text for better contrast
        activebackground="#ff1a1a",  # Darker red when the button is pressed
        activeforeground="white",    # Keep text white when pressed
        font=("Helvetica", 16, "bold"),  # Larger bold font
        relief="raised",          # 3D raised effect
        bd=4,                     # Border thickness for the button
        width=20,
        height=2                  # Slightly increase the height for a better button size
    )

    # Place the buzzer button in row 3 (below the slider)
    buzzerButton.grid(
        row=3, 
        column=0, 
        columnspan=4, 
        padx=10,  # Increase padding for better spacing
        pady=10
    )


    # Configure row/column weights for resizing behavior
    root.grid_rowconfigure(1, weight=1)  # Allow row 1 (graphs) to expand
    root.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Allow columns to expand

    # Connect hover event for the graphs
    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    return root, ax1, ax2, ax3, ax4, canvas, fig


# Main function to start the app
if __name__ == "__main__":
    # Set up the Tkinter GUI
    root, ax1, ax2, ax3, ax4, canvas, fig = setup_gui()
    
    # Set up the MQTT client
    # mqtt_client = setup_mqtt()
    
    # Start the Tkinter event loop
    root.mainloop()
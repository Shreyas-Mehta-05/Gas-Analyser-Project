import pandas as pd
import matplotlib.pyplot as plt

# Load data from feed.csv for MQ7 sensor
df = pd.read_csv('wokringdataset.csv')

# Convert 'created_at' to datetime for better plotting
df['created_at'] = pd.to_datetime(df['created_at'])

# Constants for Ps calculation
RL = 1 * 1000  # RL in ohms (1kΩ)
VC = 3.3  # Circuit voltage (3.3V)

# Calculate Ps based on the formula using Rs (from field1)
df['Ps'] = (VC**2 * df['field1']) / ((df['field1'] + RL)**2)

# Calculate moving averages (window size = 3) for MQ7
df['Rs_MA'] = df['field1'].rolling(window=3).mean()  # Moving average of Rs (sensor resistance)
df['Temperature_MA'] = df['field2'].rolling(window=3).mean()  # Moving average of temperature
df['Humidity_MA'] = df['field3'].rolling(window=3).mean()  # Moving average of humidity
df['CO_MA'] = df['field4'].rolling(window=3).mean()  # Moving average of CO concentration
df['Ps_MA'] = df['Ps'].rolling(window=3).mean()  # Moving average of power consumption (Ps)

# Optional: Downsample the data by selecting every nth row (e.g., every 5th reading)
df_downsampled = df.iloc[::2, :]

# Plot CO concentration over time (with moving average) for MQ7
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['field4'], label='CO (ppm)', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['CO_MA'], label='CO (Moving Avg)', linestyle='--')

# Label the plot
plt.title('CO Concentration Over Time (MQ7)')
plt.xlabel('Timestamp')
plt.ylabel('CO Concentration (ppm)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot sensor resistance over time (with moving average) for MQ7
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['field1'], label='Sensor Resistance (Ohm)', color='red', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Rs_MA'], label='Resistance (Moving Avg)', color='red', linestyle='--')

# Label the plot
plt.title('Sensor Resistance (Rs) Over Time (MQ7)')
plt.xlabel('Timestamp')
plt.ylabel('Resistance (Ohms)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot temperature and humidity over time (with moving averages) for MQ7
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['field2'], label='Temperature (°C)', color='blue', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Temperature_MA'], label='Temperature (Moving Avg)', color='blue', linestyle='--')
plt.plot(df_downsampled['created_at'], df_downsampled['field3'], label='Humidity (%)', color='purple', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Humidity_MA'], label='Humidity (Moving Avg)', color='purple', linestyle='--')

# Label the plot
plt.title('Temperature and Humidity Over Time (MQ7)')
plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot Ps (Power Consumption) over time (with moving average) for MQ7
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['Ps'], label='Power Consumption Ps', color='green', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Ps_MA'], label='Ps (Moving Avg)', color='green', linestyle='--')

# Label the plot
plt.title('Sensor Power Consumption (Ps) Over Time (MQ7)')
plt.xlabel('Timestamp')
plt.ylabel('Power Consumption (Ps)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

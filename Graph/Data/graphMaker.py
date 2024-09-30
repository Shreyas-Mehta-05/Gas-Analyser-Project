import pandas as pd
import matplotlib.pyplot as plt

# Load data from feed.csv
df = pd.read_csv('feed.csv')

# Convert 'created_at' to datetime for better plotting
df['created_at'] = pd.to_datetime(df['created_at'])

# Constants for Ps calculation
RL = 5.0 * 1000  # RL in ohms (5kΩ)
VC = 5.0  # Circuit voltage (5V)

# Calculate Ps based on the formula
df['Ps'] = ((df['field4'] + RL)**2 * VC**2) / df['field4']

# Calculate moving averages (window size = 3)
df['LPG_MA'] = df['field1'].rolling(window=3).mean()
df['CO_MA'] = df['field2'].rolling(window=3).mean()
df['Smoke_MA'] = df['field3'].rolling(window=3).mean()
df['Resistance_MA'] = df['field4'].rolling(window=3).mean()
df['Ps_MA'] = df['Ps'].rolling(window=3).mean()

# Optional: Downsample the data by selecting every nth row (e.g., every 5th reading)
df_downsampled = df.iloc[::2, :]

# Plot LPG, CO, Smoke concentrations over time (with moving average)
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['field1'], label='LPG (ppm)', marker='o', alpha=0.6)
plt.plot(df_downsampled['created_at'], df_downsampled['field2'], label='CO (ppm)', marker='o', alpha=0.6)
plt.plot(df_downsampled['created_at'], df_downsampled['field3'], label='Smoke (ppm)', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['LPG_MA'], label='LPG (Moving Avg)', linestyle='--')
plt.plot(df['created_at'], df['CO_MA'], label='CO (Moving Avg)', linestyle='--')
plt.plot(df['created_at'], df['Smoke_MA'], label='Smoke (Moving Avg)', linestyle='--')

# Label the plot
plt.title('Gas Concentrations Over Time (Downsampled and Smoothed)')
plt.xlabel('Timestamp')
plt.ylabel('Concentration (ppm)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot sensor resistance over time (with moving average)
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['field4'], label='Sensor Resistance (Ohm)', color='red', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Resistance_MA'], label='Resistance (Moving Avg)', color='red', linestyle='--')
# calculate mean and variance

# Label the plot
plt.title('Sensor Resistance Over Time (Downsampled and Smoothed)')
plt.xlabel('Timestamp')
plt.ylabel('Resistance (Ohms)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot Ps (Power Consumption) over time (with moving average)
plt.figure(figsize=(10, 6))
plt.plot(df_downsampled['created_at'], df_downsampled['Ps'], label='Power Consumption Ps', color='green', marker='o', alpha=0.6)
plt.plot(df['created_at'], df['Ps_MA'], label='Ps (Moving Avg)', color='green', linestyle='--')

# Label the plot
plt.title('Sensor Power Consumption (Ps) Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Power Consumption (Ps)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

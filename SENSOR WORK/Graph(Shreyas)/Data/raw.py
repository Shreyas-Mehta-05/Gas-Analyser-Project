import pandas as pd
import matplotlib.pyplot as plt

# Load data from feed.csv
df = pd.read_csv('feed.csv')

# Convert 'created_at' to datetime for better plotting
df['created_at'] = pd.to_datetime(df['created_at'])

# Constants for Ps calculation
RL = 5.0 * 1000  # RL in ohms (5kΩ)
VC = 5.0  # Circuit voltage (5V)
df['Ps'] = ((df['field4'] + RL)**2 * VC**2) / df['field4']

# Define the window size for moving average and EMA
window_size = 3  # For moving average
ema_span = 10    # For EMA

# Calculate moving averages
df['field1_MA'] = df['field1'].rolling(window=window_size).mean()
df['field2_MA'] = df['field2'].rolling(window=window_size).mean()
df['field3_MA'] = df['field3'].rolling(window=window_size).mean()
df['field4_MA'] = df['field4'].rolling(window=window_size).mean()

# Calculate EMA for Ps
df['Ps_EMA'] = df['Ps'].ewm(span=ema_span, adjust=False).mean()

# Define a function to plot lines, markers, and moving averages
def plot_with_lines_and_moving_avg(x, y, y_ma, label, color, marker='o'):
    # Create a mask to filter out zeros
    mask = y > 0
    # Plot the data with lines and markers for non-zero values
    plt.plot(x[mask], y[mask], label=f'{label} (Actual)', color=color, marker=marker, linestyle='-', alpha=0.6)
    plt.plot(x[mask], y_ma[mask], label=f'{label} (Moving Avg)', color=color, linestyle='--', alpha=0.6)
    plt.scatter(x[mask], y[mask], color=color, marker=marker, alpha=0.6)

# Plot LPG, CO, Smoke concentrations over time with lines, circles, and moving averages
plt.figure(figsize=(10, 6))
plot_with_lines_and_moving_avg(df['created_at'], df['field1'], df['field1_MA'], 'LPG (ppm)', 'blue')
plot_with_lines_and_moving_avg(df['created_at'], df['field2'], df['field2_MA'], 'CO (ppm)', 'orange')
plot_with_lines_and_moving_avg(df['created_at'], df['field3'], df['field3_MA'], 'Smoke (ppm)', 'green')

# Label the plot
plt.title('Gas Concentrations Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Concentration (ppm)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot sensor resistance over time with lines, circles, and moving averages
plt.figure(figsize=(10, 6))
plot_with_lines_and_moving_avg(df['created_at'], df['field4'], df['field4_MA'], 'Sensor Resistance (Ohm)', 'red')

# Label the plot
plt.title('Sensor Resistance Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Resistance (Ohms)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Plot Ps (Power Consumption) over time with lines, circles, and EMA
plt.figure(figsize=(10, 6))
plot_with_lines_and_moving_avg(df['created_at'], df['Ps'], df['Ps_EMA'], 'Power Consumption Ps', 'green', marker='o')

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

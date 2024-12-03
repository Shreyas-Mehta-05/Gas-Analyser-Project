
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
data = pd.read_csv('caliberation.csv')

# Extract relevant fields for each sensor and drop NaN values
mq7_rs = data['field1'].dropna()
mq7_ppm = data['field2'].dropna()
mq9_rs = data['field3'].dropna()
mq9_ppm = data['field4'].dropna()
mq136_rs = data['field5'].dropna()
mq136_ppm = data['field6'].dropna()
temperature = data['field7'].dropna()
humidity = data['field8'].dropna()

# Define a function to calculate moving average
def moving_average(data, window_size):
    return data.rolling(window=window_size, min_periods=1).mean()  # Use min_periods to ensure no NaN in moving average

def getRs(Rl, Vrl,Vc = 3.3):
    # Rl=load resistance, Vrl=voltage across load resistance
     # voltage of the circuit
    return Rl * (Vc - Vrl) / Vrl

def getVrl(Rl, Rs, Vc=3.3):
    # Rl = load resistance, Rs = sensor resistance, Vc = circuit voltage
    return (Rl * Vc) / (Rs + Rl)

def getVrl(Rl, Rs, Vc=3.3):
    # Rl = load resistance, Rs = sensor resistance, Vc = circuit voltage
    return (Rl * Vc) / (Rs + Rl)
def getPower(Rs,Rl,Vc=3.3):
    return (Vc**2)*(Rs/((Rs+Rl)**2))

def f_mq9(T, H):
    # Coefficients from regression for MQ9
    a = 1.2636396581018856
    b1 = -0.015411273502357305
    b2 = 0.0001423447717815803
    b3 = -2.667160028389554e-07
    b4 = -3.147248816276855e-05
    b5 = 3.5955470516473796e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq9(ppm):
    return 23.743*(ppm**(-0.461))

def formula_mq9(H, T, Rs_mq9, Ro_mq9=2962.049073305054):
    return (963.40351 * (Rs_mq9 / Ro_mq9)**(-2.16919739696)) * (f_mq9(20, 65) / f_mq9(T, H))**(-2.16919739696)

# MQ7 functions
def f_mq7(T, H):
    # Coefficients from regression for MQ7
    a = 1.2094342542500245
    b1 = -0.01094546624860255
    b2 = 8.559231727624334e-05
    b3 = -2.220918787838429e-07
    b4 = -2.6206841578149175e-05
    b5 = 1.4963577356169694e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq7(ppm):
    a = 22.679
    b = -0.676
    return a * (ppm**b)

def formula_mq7(H, T, Rs, Ro=2962.049073305054):
    return (101.24201 * (Rs / Ro)**(-1.4792899)) * (f_mq7(20, 65) / f_mq7(T, H))**(-1.4792899)

# MQ136 functions
def f_mq136(T, H):
    # Coefficients from regression for MQ136
    a = 1.8049213062479526
    b1 = -0.01676578961983332
    b2 = 2.2683055653041216e-05
    b3 = -0.008472631405786416
    b4 = 8.707501494816326e-06
    b5 = 6.712560534401002e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq136(ppm):
    return 0.585 * (ppm**(-0.267))

def formula_mq136(H, T, Rs_mq136, Ro_mq136=2962.049073305054):
    return (0.1342531 * (Rs_mq136 / Ro_mq136)**(-3.74531835206)) * (f_mq136(20, 65) / f_mq136(T, H))**(-3.74531835206)



    
corrected_mq9_Rl =500
miscaled_mq9_Rl = 1000
for i in range(len(mq9_rs)):
    # Access the value at index i using .iloc
    mq9_rs.iloc[i] = getRs(corrected_mq9_Rl, getVrl(miscaled_mq9_Rl, mq9_rs.iloc[i]))

# we actually send the Rs/Ro value to the thingspeak for mq7 so we will recalculate the Rs value
for i in range(len(mq7_rs)):
    mq7_rs.iloc[i] = 385.73 * (mq7_rs.iloc[i])

# for i in range(len(mq9_rs)):
#     mq9_rs.iloc[i] = 1 * (mq9_rs.iloc[i])
# Set window size for moving average
window_size = 30  # You can customize this value

# Compute moving averages for Rs values of each sensor, ignoring NaN values
mq7_rs_ma = moving_average(mq7_rs, window_size)
mq9_rs_ma = moving_average(mq9_rs, window_size)
mq136_rs_ma = moving_average(mq136_rs, window_size)

# Set a common style for the plots
# plt.style.use('seaborn-darkgrid')
plt.style.use('ggplot')

# Plotting Rs and Moving Averages
plt.figure(figsize=(12, 10))

# Customize color palette
colors = ['#FF6F61', '#6B5B95', '#88B04B']

# Define a function to downsample data (e.g., take every nth data point)
def downsample(data, factor):
    return data[::factor]

# Set downsampling factor to reduce the density (try a factor like 5 or 10)
downsample_factor = 5

# Downsample Rs and ppm data
mq7_rs_downsampled = downsample(mq7_rs, downsample_factor)
mq7_ppm_downsampled = downsample(mq7_ppm, downsample_factor)
mq9_rs_downsampled = downsample(mq9_rs, downsample_factor)
mq9_ppm_downsampled = downsample(mq9_ppm, downsample_factor)
mq136_rs_downsampled = downsample(mq136_rs, downsample_factor)
mq136_ppm_downsampled = downsample(mq136_ppm, downsample_factor)

# Moving averages for ppm as well
mq7_ppm_ma = moving_average(mq7_ppm, window_size)
mq9_ppm_ma = moving_average(mq9_ppm, window_size)
mq136_ppm_ma = moving_average(mq136_ppm, window_size)

# Re-plotting Rs with downsampled data
# plt.figure(figsize=(12, 10))

# Plot for MQ7 Rs
plt.subplot(3, 1, 1)
plt.plot(mq7_rs_downsampled.index, mq7_rs_downsampled, label='MQ7 Rs (Downsampled)', color=colors[0], linewidth=1.5)
plt.plot(mq7_rs_ma.index, mq7_rs_ma, label=f'MQ7 Rs (MA, window={window_size})', linestyle='--', color=colors[0], linewidth=2, alpha=0.7)
plt.title('MQ7 Sensor Rs (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('Rs', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

# Plot for MQ9 Rs
plt.subplot(3, 1, 2)
plt.plot(mq9_rs_downsampled.index, mq9_rs_downsampled, label='MQ9 Rs (Downsampled)', color=colors[1], linewidth=1.5)
plt.plot(mq9_rs_ma.index, mq9_rs_ma, label=f'MQ9 Rs (MA, window={window_size})', linestyle='--', color=colors[1], linewidth=2, alpha=0.7)
plt.title('MQ9 Sensor Rs (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('Rs', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

# Plot for MQ136 Rs
plt.subplot(3, 1, 3)
plt.plot(mq136_rs_downsampled.index, mq136_rs_downsampled, label='MQ136 Rs (Downsampled)', color=colors[2], linewidth=1.5)
plt.plot(mq136_rs_ma.index, mq136_rs_ma, label=f'MQ136 Rs (MA, window={window_size})', linestyle='--', color=colors[2], linewidth=2, alpha=0.7)
plt.title('MQ136 Sensor Rs (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('Rs', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

plt.tight_layout()
plt.savefig('Rs_MA_downscaled.png')
plt.show()

# Re-plotting ppm with moving averages
plt.figure(figsize=(12, 10))

# Plot for MQ7 ppm
plt.subplot(3, 1, 1)
plt.plot(mq7_ppm_downsampled.index, mq7_ppm_downsampled, label='MQ7 ppm (Downsampled)', color=colors[0], linewidth=1.5)
plt.plot(mq7_ppm_ma.index, mq7_ppm_ma, label=f'MQ7 ppm (MA, window={window_size})', linestyle='--', color=colors[0], linewidth=2, alpha=0.7)
plt.title('MQ7 Sensor ppm (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('ppm', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

# Plot for MQ9 ppm
plt.subplot(3, 1, 2)
plt.plot(mq9_ppm_downsampled.index, mq9_ppm_downsampled, label='MQ9 ppm (Downsampled)', color=colors[1], linewidth=1.5)
plt.plot(mq9_ppm_ma.index, mq9_ppm_ma, label=f'MQ9 ppm (MA, window={window_size})', linestyle='--', color=colors[1], linewidth=2, alpha=0.7)
plt.title('MQ9 Sensor ppm (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('ppm', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

# Plot for MQ136 ppm
plt.subplot(3, 1, 3)
plt.plot(mq136_ppm_downsampled.index, mq136_ppm_downsampled, label='MQ136 ppm (Downsampled)', color=colors[2], linewidth=1.5)
plt.plot(mq136_ppm_ma.index, mq136_ppm_ma, label=f'MQ136 ppm (MA, window={window_size})', linestyle='--', color=colors[2], linewidth=2, alpha=0.7)
plt.title('MQ136 Sensor ppm (Downsampled) and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('ppm', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)

plt.tight_layout()
plt.savefig('ppm_MA_downscaled.png')
plt.show()



# now we will plot the Ro
def calculate_Ro_mq9(Rs_mq9, ppm, T, H):
    """
    Calculate Ro for MQ9 sensor.
    
    Args:
    Rs_mq9: Measured resistance of the MQ9 sensor in ohms.
    ppm: Concentration of gas in ppm.
    T: Temperature in degrees Celsius.
    H: Humidity in percentage.

    Returns:
    calculatedRo_mq9: Calculated Ro value for MQ9 sensor.
    """
    experimentVal_mq9 = getRatio_mq9(ppm) * f_mq9(T, H) / f_mq9(20, 65)
    calculatedRo_mq9 = Rs_mq9 / experimentVal_mq9
    return calculatedRo_mq9

def calculate_Ro_mq7(Rs_mq7, ppm, T, H):
    """
    Calculate Ro for MQ7 sensor.
    
    Args:
    Rs_mq7: Measured resistance of the MQ7 sensor in ohms.
    ppm: Concentration of gas in ppm.
    T: Temperature in degrees Celsius.
    H: Humidity in percentage.

    Returns:
    calculatedRo_mq7: Calculated Ro value for MQ7 sensor.
    """
    experimentVal_mq7 = getRatio_mq7(ppm) * f_mq7(T, H) / f_mq7(20, 65)
    calculatedRo_mq7 = Rs_mq7 / experimentVal_mq7
    return calculatedRo_mq7

def calculate_Ro_mq136(Rs_mq136, ppm, T, H):
    """
    Calculate Ro for MQ136 sensor.
    
    Args:
    Rs_mq136: Measured resistance of the MQ136 sensor in ohms.
    ppm: Concentration of gas in ppm.
    T: Temperature in degrees Celsius.
    H: Humidity in percentage.

    Returns:
    calculatedRo_mq136: Calculated Ro value for MQ136 sensor.
    """
    experimentVal_mq136 = getRatio_mq136(ppm) * f_mq136(T, H) / f_mq136(20, 65)
    calculatedRo_mq136 = Rs_mq136 / experimentVal_mq136
    return calculatedRo_mq136


import matplotlib.pyplot as plt

# # Sample data: Replace with your actual data arrays for Rs
# mq7_rs = ...  # Your actual DataFrame or list for MQ7 Rs values
# mq9_rs = ...  # Your actual DataFrame or list for MQ9 Rs values
# mq136_rs = ...  # Your actual DataFrame or list for MQ136 Rs values
# temperature = ...  # Your actual DataFrame or list for temperature values
# humidity = ...  # Your actual DataFrame or list for humidity values

# Calculate Ro for each sensor
mq7_Ro = [calculate_Ro_mq7(mq7_rs.iloc[i], 7, temperature.iloc[i], humidity.iloc[i]) for i in range(len(mq7_rs))]
mq9_Ro = [calculate_Ro_mq9(mq9_rs.iloc[i], 0.3, temperature.iloc[i], humidity.iloc[i]) for i in range(len(mq9_rs))]
mq136_Ro = [calculate_Ro_mq136(mq136_rs.iloc[i], 0.1, temperature.iloc[i], humidity.iloc[i]) for i in range(len(mq136_rs))]

# downsample Ro values
mq7_Ro_downsampled = downsample(mq7_Ro, downsample_factor)
mq9_Ro_downsampled = downsample(mq9_Ro, downsample_factor)
mq136_Ro_downsampled = downsample(mq136_Ro, downsample_factor)
# Plot Ro values for each sensor in subplots
plt.figure(figsize=(12, 10))

# MQ7 plot
plt.subplot(3, 1, 1)
plt.plot(mq7_Ro_downsampled, label='MQ7 Ro', color=colors[0], linewidth=1.5)
plt.title('MQ7 Sensor Ro for ppm=7', fontsize=16, fontweight='bold')
# plt.text(0, mq7_Ro_downsampled[0], 'ppm = 7', fontsize=8, color='black')
# we will add a label for ppm = 7 by adding the legend
plt.legend(['ppm = 7'], loc='upper right', fontsize=10, title='MQ7 ppm')

plt.xlabel('Time (Index)', fontsize=14)
plt.ylabel('Ro (Ohm)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# MQ9 plot
plt.subplot(3, 1, 2)
plt.plot(mq9_Ro_downsampled, label='MQ9 Ro', color=colors[1], linewidth=1.5)
plt.title('MQ9 Sensor Ro for ppm=0.3', fontsize=16, fontweight='bold')
# plt.text(0, mq9_Ro_downsampled[0], 'ppm = 0.3', fontsize=8, color='black')
plt.legend(['ppm = 0.3'], loc='upper right', fontsize=10, title='MQ9 ppm')
plt.xlabel('Time (Index)', fontsize=14)
plt.ylabel('Ro (Ohm)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# MQ136 plot
plt.subplot(3, 1, 3)
plt.plot(mq136_Ro_downsampled, label='MQ136 Ro', color=colors[2], linewidth=1.5)
plt.title('MQ136 Sensor Ro for ppm=0.1', fontsize=16, fontweight='bold')
# add a lable for ppm = 0.1
# plt.text(0, mq136_Ro_downsampled[0], 'ppm = 0.1', fontsize=8, color=colors[2])
plt.legend(['ppm = 0.1'], loc='upper right', fontsize=10, title='MQ136 ppm')

plt.xlabel('Time (Index)', fontsize=14)
plt.ylabel('Ro (Ohm)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.savefig('Ro_downscaled.png')
plt.show()

## now we will plot the Power
def calculate_Power(Rs, Rl, Vc=3.3):
    """
    Calculate power dissipated by the sensor.
    
    Args:
    Rs: Measured resistance of the sensor in ohms.
    Rl: Load resistance in ohms.
    Vc: Circuit voltage in volts (default is 3.3V).

    Returns:
    power: Power dissipated by the sensor in watts.
    """
    return (Vc**2) * (Rs / ((Rs + Rl)**2))

# Calculate power for each sensor
mq7_power = [calculate_Power(mq7_rs.iloc[i], 1000) for i in range(len(mq7_rs))]
mq9_power = [calculate_Power(mq9_rs.iloc[i], 500) for i in range(len(mq9_rs))]
mq136_power = [calculate_Power(mq136_rs.iloc[i], 1000) for i in range(len(mq136_rs))]
               
# downsample power values
mq7_power_downsampled = downsample(mq7_power, downsample_factor)
mq9_power_downsampled = downsample(mq9_power, downsample_factor)
mq136_power_downsampled = downsample(mq136_power, downsample_factor)

import pandas as pd

def movingaverage(data, window_size):
    """
    Calculate the moving average of the given data.

    Args:
    data: List of numerical values.
    window_size: Size of the moving average window.

    Returns:
    List of moving averages.
    """
    series = pd.Series(data)  # Convert list to pandas Series
    return series.rolling(window=window_size, min_periods=1).mean().tolist()  # Return as list

               
# calculate moving average for power
mq7_power_ma = movingaverage(mq7_power_downsampled, window_size)
mq9_power_ma = movingaverage(mq9_power_downsampled, window_size)
mq136_power_ma = movingaverage(mq136_power_downsampled, window_size)

# Plot Power values for each sensor in subplots
plt.figure(figsize=(12, 10))

# MQ7 Power plot
plt.subplot(3, 1, 1)
plt.plot(mq7_power_downsampled, label='MQ7 Power', color=colors[0], linewidth=1.5)
# Plot moving average
plt.plot(mq7_power_ma, label='MQ7 Power (MA)', linestyle='--', color=colors[0], linewidth=2, alpha=0.7)
plt.title('MQ7 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# MQ9 Power plot
plt.subplot(3, 1, 2)
plt.plot(mq9_power_downsampled, label='MQ9 Power', color=colors[1], linewidth=1.5)
# Plot moving average
plt.plot(mq9_power_ma, label='MQ9 Power (MA)', linestyle='--', color=colors[1], linewidth=2, alpha=0.7)
plt.title('MQ9 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# MQ136 Power plot
plt.subplot(3, 1, 3)
plt.plot(mq136_power_downsampled, label='MQ136 Power', color=colors[2], linewidth=1.5)
# Plot moving average
plt.plot(mq136_power_ma, label='MQ136 Power (MA)', linestyle='--', color=colors[2], linewidth=2, alpha=0.7)
plt.title('MQ136 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.savefig('Power_MA_downscaled.png')
plt.show()


# Now for each sensor plot the Rs Power ppm vs time
# Plot Rs, Power, and ppm values for each sensor in subplots
plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
plt.plot(mq7_rs_downsampled, label='MQ7 Rs', color=colors[0], linewidth=1.5)
plt.suptitle('Sensor Data Analysis', fontsize=18, fontweight='bold')
plt.title('MQ7 Sensor Rs, Power, and ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Rs', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(3, 1, 2)
plt.plot(mq7_power_downsampled, label='MQ7 Power', color=colors[1], linewidth=1.5)
plt.title('MQ7 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(3, 1, 3)
plt.plot(mq7_ppm_downsampled, label='MQ7 ppm', color=colors[2], linewidth=1.5)
plt.title('MQ7 Sensor ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('ppm', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.savefig('MQ7_Rs_Power_ppm_downscaled.png')
plt.show()

# Plot Rs, Power, and ppm values for each sensor in subplots
plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
plt.plot(mq9_rs_downsampled, label='MQ9 Rs', color=colors[0], linewidth=1.5)
plt.suptitle('Sensor Data Analysis', fontsize=18, fontweight='bold')
plt.title('MQ9 Sensor Rs, Power, and ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Rs', fontsize=14)
plt.grid(True)
plt.legend(loc='upper right')

plt.subplot(3, 1, 2)
plt.plot(mq9_power_downsampled, label='MQ9 Power', color=colors[1], linewidth=1.5)
plt.title('MQ9 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(mq9_ppm_downsampled, label='MQ9 ppm', color=colors[2], linewidth=1.5)
plt.title('MQ9 Sensor ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('ppm', fontsize=14)
plt.grid(True)

plt.tight_layout()
plt.savefig('MQ9_Rs_Power_ppm_downscaled.png')
plt.show()

# Plot Rs, Power, and ppm values for each sensor in subplots

plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
plt.plot(mq136_rs_downsampled, label='MQ136 Rs', color=colors[0], linewidth=1.5)
plt.suptitle('Sensor Data Analysis', fontsize=18, fontweight='bold')
plt.title('MQ136 Sensor Rs, Power, and ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Rs', fontsize=14)

plt.grid(True)
plt.legend(loc='upper right')

plt.subplot(3, 1, 2)
plt.plot(mq136_power_downsampled, label='MQ136 Power', color=colors[1], linewidth=1.5)
plt.title('MQ136 Sensor Power', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('Power (W)', fontsize=14)
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(mq136_ppm_downsampled, label='MQ136 ppm', color=colors[2], linewidth=1.5)
plt.title('MQ136 Sensor ppm', fontsize=16, fontweight='bold')
plt.xlabel('Sample Index', fontsize=14)
plt.ylabel('ppm', fontsize=14)
plt.grid(True)


plt.tight_layout()
plt.savefig('MQ136_Rs_Power_ppm_downscaled.png')
plt.show()




               





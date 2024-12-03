import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load data from feed.csv
df = pd.read_csv('feed.csv')

# Ro value from calibration
Ro = 11.82  # in kilo-ohms

# Replace 'inf' values with NaN and then drop NaNs
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Calculate Rs/Ro for LPG, CO, and Smoke based on field4
df['LPG_RsRo'] = df['field4'] / Ro
df['CO_RsRo'] = df['field4'] / Ro
df['Smoke_RsRo'] = df['field4'] / Ro

# Concentrations for LPG, CO, and Smoke (fields field1, field2, field3)
lpg_concentration = df['field1']
co_concentration = df['field2']
smoke_concentration = df['field3']

# Convert Rs/Ro and concentration to logarithmic scale
log_LPG_RsRo = np.log10(df['LPG_RsRo'].replace(0, np.nan))  # Replace 0 with NaN to avoid log(0) error
log_CO_RsRo = np.log10(df['CO_RsRo'].replace(0, np.nan))
log_Smoke_RsRo = np.log10(df['Smoke_RsRo'].replace(0, np.nan))

log_lpg_concentration = np.log10(lpg_concentration + 1e-10)  # Avoid log(0) error
log_co_concentration = np.log10(co_concentration + 1e-10)
log_smoke_concentration = np.log10(smoke_concentration + 1e-10)

# Filter data to include only concentrations between 0.1 and 100 ppm
lpg_mask = (lpg_concentration >= 0.1) & (lpg_concentration <= 1000)
co_mask = (co_concentration >= 0.01) & (co_concentration <= 100)
smoke_mask = (smoke_concentration >= 0.1) & (smoke_concentration <= 1000)

# Filtered data
filtered_log_lpg_concentration = log_lpg_concentration[lpg_mask]
filtered_log_CO_concentration = log_co_concentration[co_mask]
filtered_log_smoke_concentration = log_smoke_concentration[smoke_mask]

filtered_log_LPG_RsRo = log_LPG_RsRo[lpg_mask]
filtered_log_CO_RsRo = log_CO_RsRo[co_mask]
filtered_log_Smoke_RsRo = log_Smoke_RsRo[smoke_mask]

# Apply linear regression to filtered data for LPG, CO, Smoke
def linear_regression(x, y):
    # Ensure no NaN or infinite values in input
    valid_indices = np.isfinite(x) & np.isfinite(y)
    x = x[valid_indices]
    y = y[valid_indices]
    
    if len(x) == 0:
        raise ValueError("No valid data points available for regression.")

    x = x.values.reshape(-1, 1)  # Reshape for sklearn
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    return y_pred, model.coef_[0], model.intercept_

# Perform regression for LPG
try:
    lpg_pred, lpg_slope, lpg_intercept = linear_regression(filtered_log_lpg_concentration, filtered_log_LPG_RsRo)
except ValueError as e:
    print(f"Error performing regression for LPG: {e}")
    lpg_pred, lpg_slope, lpg_intercept = np.nan, np.nan, np.nan

# Perform regression for CO
try:
    co_pred, co_slope, co_intercept = linear_regression(filtered_log_CO_concentration, filtered_log_CO_RsRo)
except ValueError as e:
    print(f"Error performing regression for CO: {e}")
    co_pred, co_slope, co_intercept = np.nan, np.nan, np.nan

# Perform regression for Smoke
try:
    smoke_pred, smoke_slope, smoke_intercept = linear_regression(filtered_log_smoke_concentration, filtered_log_Smoke_RsRo)
except ValueError as e:
    print(f"Error performing regression for Smoke: {e}")
    smoke_pred, smoke_slope, smoke_intercept = np.nan, np.nan, np.nan

# Define a range for extrapolation
concentration_range = np.logspace(-2, 2.5, 500)  # From 0.1 to 1000 ppm

# Extrapolate using the regression models
def extrapolate(concentration, slope, intercept):
    log_concentration = np.log10(concentration + 1e-10)  # Avoid log(0) error
    return 10**(slope * log_concentration + intercept)

# LPG extrapolation
if not np.isnan(lpg_slope):
    lpg_extrapolated = extrapolate(concentration_range, lpg_slope, lpg_intercept)

# CO extrapolation
if not np.isnan(co_slope):
    co_extrapolated = extrapolate(concentration_range, co_slope, co_intercept)

# Smoke extrapolation
if not np.isnan(smoke_slope):
    smoke_extrapolated = extrapolate(concentration_range, smoke_slope, smoke_intercept)

# Plot separate graphs for each gas with extrapolation

# concentration_range = np.logspace(-1.5, 2.5, 500)  # From 0.01 to 1000 ppm

# Extrapolate using the regression models
def extrapolate(concentration, slope, intercept):
    log_concentration = np.log10(concentration + 1e-10)  # Avoid log(0) error
    return 10**(slope * log_concentration + intercept)

# LPG extrapolation
if not np.isnan(lpg_slope):
    lpg_extrapolated = extrapolate(concentration_range, lpg_slope, lpg_intercept)

# CO extrapolation
if not np.isnan(co_slope):
    co_extrapolated = extrapolate(concentration_range, co_slope, co_intercept)

# Smoke extrapolation
if not np.isnan(smoke_slope):
    smoke_extrapolated = extrapolate(concentration_range, smoke_slope, smoke_intercept)

# Plot separate graphs for each gas with extrapolation

# LPG plot
plt.figure(figsize=(10, 6))
plt.plot(10**filtered_log_lpg_concentration, 10**filtered_log_LPG_RsRo, 'o', label='LPG Data', markersize=5)
if not np.isnan(lpg_slope):
    plt.plot(concentration_range, lpg_extrapolated, '--', label=f'LPG Regression (Slope: {lpg_slope:.2f})')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Concentration in ppm')
plt.ylabel('Rs/Ro')
plt.title('LPG: Log Rs/Ro vs Log Concentration')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()

# CO plot
plt.figure(figsize=(10, 6))
plt.plot(10**filtered_log_CO_concentration, 10**filtered_log_CO_RsRo, 'o', label='CO Data', markersize=5)
if not np.isnan(co_slope):
    plt.plot(concentration_range, co_extrapolated, '--', label=f'CO Regression (Slope: {co_slope:.2f})')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Concentration in ppm')
plt.ylabel('Rs/Ro')
plt.title('CO: Log Rs/Ro vs Log Concentration')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()

# Smoke plot
plt.figure(figsize=(10, 6))
plt.plot(10**filtered_log_smoke_concentration, 10**filtered_log_Smoke_RsRo, 'o', label='Smoke Data', markersize=5)
if not np.isnan(smoke_slope):
    plt.plot(concentration_range, smoke_extrapolated, '--', label=f'Smoke Regression (Slope: {smoke_slope:.2f})')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Concentration in ppm')
plt.ylabel('Rs/Ro')
plt.title('Smoke: Log Rs/Ro vs Log Concentration')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
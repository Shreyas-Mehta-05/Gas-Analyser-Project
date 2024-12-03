import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import mean_squared_error

# Load the data from the CSV file
df_combined = pd.read_csv('TestData.csv')

# Assign humidity values based on the column
df_30 = df_combined[['Temperature', 'Ratio_30%']].copy()
df_30['Humidity'] = 30
df_30 = df_30.rename(columns={'Ratio_30%': 'Rs_Ro'})

df_60 = df_combined[['Temperature', 'Ratio_60%']].copy()
df_60['Humidity'] = 60
df_60 = df_60.rename(columns={'Ratio_60%': 'Rs_Ro'})

# Load the 85% humidity data
df_85 = df_combined[['Temperature', 'Ratio_85%']].copy()
df_85['Humidity'] = 85
df_85 = df_85.rename(columns={'Ratio_85%': 'Rs_Ro'})

# Combine all datasets
df_all = pd.concat([df_30, df_60, df_85], ignore_index=True)

# Prepare the polynomial features: T, T^2, H, H^2, and TH
df_all['T^2'] = df_all['Temperature'] ** 2
df_all['H^2'] = df_all['Humidity'] ** 2
df_all['TH'] = df_all['Temperature'] * df_all['Humidity']

# Prepare the features and target
X = df_all[['Temperature', 'T^2', 'Humidity', 'H^2', 'TH']]
y = df_all['Rs_Ro']

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Print the coefficients
print("General Equation: Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH")
print("Where:")
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# For visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot of the actual data
ax.scatter(df_all['Temperature'], df_all['Humidity'], df_all['Rs_Ro'], color='r', label='Data Points')

# Generate grid for predictions
T_range = np.linspace(df_all['Temperature'].min(), df_all['Temperature'].max(), 100)
H_range = np.linspace(30, 85, 100)  # Covering 30% to 85% humidity
T_grid, H_grid = np.meshgrid(T_range, H_range)

# Create the same polynomial features for the grid
T2_grid = T_grid ** 2
H2_grid = H_grid ** 2
TH_grid = T_grid * H_grid

# Predict Rs/Ro over the grid
grid_data = pd.DataFrame({
    'Temperature': T_grid.flatten(),
    'T^2': T2_grid.flatten(),
    'Humidity': H_grid.flatten(),
    'H^2': H2_grid.flatten(),
    'TH': TH_grid.flatten()
})

Z = model.predict(grid_data)

# Reshape Z back into the grid shape for plotting
Z = Z.reshape(T_grid.shape)

# Plot the surface
ax.plot_surface(T_grid, H_grid, Z, alpha=0.5)

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Humidity (%)')
ax.set_zlabel('Rs/Ro')
ax.set_title('Surface Fit of Rs/Ro Based on Temperature and Humidity')
ax.legend()
plt.show()

# Calculate and print R-squared and adjusted R-squared
r_squared = model.score(X, y)
print("R-squared:", r_squared)

n = X.shape[0]
p = X.shape[1]
adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
print("Adjusted R-squared:", adjusted_r_squared)

# Calculate Mean Squared Error
y_pred = model.predict(X)
mse = mean_squared_error(y, y_pred)
print("Mean Squared Error:", mse)



print("Predicted Z values range:", Z.min(), Z.max())

plt.hist(df_all['Rs_Ro'], bins=20)
plt.title('Distribution of Rs/Ro')
plt.xlabel('Rs/Ro')
plt.ylabel('Frequency')
plt.show()


# Output correlation function coefficients
print("\nCorrelation function coefficients")
print(f"Estimated a: {model.intercept_}")
print(f"Estimated b1: {model.coef_[0]}")
print(f"Estimated b2: {model.coef_[1]}")
print(f"Estimated b3: {model.coef_[2]}")
print(f"Estimated b4: {model.coef_[3]}")
print(f"Estimated b5: {model.coef_[4]}\n")

# plot 2d-graph with T constant
T = 25
H_range = np.linspace(30, 85, 100)
T_grid = np.full_like(H_range, T)
T2_grid = T_grid ** 2
H2_grid = H_range ** 2
TH_grid = T_grid * H_range


grid_data = pd.DataFrame({
    'Temperature': T_grid.flatten(),
    'T^2': T2_grid.flatten(),
    'Humidity': H_range,
    'H^2': H2_grid.flatten(),
    'TH': TH_grid.flatten()
})

Z = model.predict(grid_data)

plt.plot(H_range, Z, label=f'Temperature = {T}°C')
plt.xlabel('Humidity (%)')
plt.ylabel('Rs/Ro')
plt.title('Rs/Ro vs Humidity at Constant Temperature')
plt.legend()
plt.grid(True)
plt.show()

# plot 2d-graph with H constant
H = 60
T_range = np.linspace(df_all['Temperature'].min(), df_all['Temperature'].max(), 100)
H_grid = np.full_like(T_range, H)
T2_grid = T_range ** 2
H2_grid = H_grid ** 2
TH_grid = T_range * H_grid

grid_data = pd.DataFrame({
    'Temperature': T_range,
    'T^2': T2_grid,
    'Humidity': H_grid.flatten(),
    'H^2': H2_grid.flatten(),
    'TH': TH_grid.flatten()
})

Z = model.predict(grid_data)

plt.plot(T_range, Z, label=f'Humidity = {H}%')
plt.xlabel('Temperature (°C)')
plt.ylabel('Rs/Ro')
plt.title('Rs/Ro vs Temperature at Constant Humidity')
plt.legend()
plt.grid(True)
plt.show()


# plot 2d-graph with T constant using the general equation as a quadratic function
# Plot Rs/Ro vs Humidity at constant Temperature (using the quadratic equation)
T = 25
H_range = np.linspace(30, 85, 100)
# Using the general quadratic equation for Rs/Ro
# Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*T*H
a = model.intercept_
b1, b2, b3, b4, b5 = model.coef_

# Compute Rs/Ro for each humidity value
Rs_Ro = a + b1 * T + b2 * (T**2) + b3 * H_range + b4 * (H_range**2) + b5 * T * H_range

plt.plot(H_range, Rs_Ro, label=f'Temperature = {T}°C (Quadratic Fit)')
plt.xlabel('Humidity (%)')
plt.ylabel('Rs/Ro')
plt.title('Rs/Ro vs Humidity at Constant Temperature (Quadratic Fit)')
plt.legend()
plt.grid(True)
plt.show()

# Plot Rs/Ro vs Temperature at constant Humidity (using the quadratic equation)
H = 60
T_range = np.linspace(df_all['Temperature'].min(), df_all['Temperature'].max(), 100)
# Using the general quadratic equation for Rs/Ro
# Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*T*H

# Compute Rs/Ro for each temperature value
Rs_Ro = a + b1 * T_range + b2 * (T_range**2) + b3 * H + b4 * (H**2) + b5 * T_range * H

plt.plot(T_range, Rs_Ro, label=f'Humidity = {H}% (Quadratic Fit)')
plt.xlabel('Temperature (°C)')
plt.ylabel('Rs/Ro')
plt.title('Rs/Ro vs Temperature at Constant Humidity (Quadratic Fit)')
plt.legend()
plt.grid(True)
plt.show()


# can be plotted using the general equation as a quadratic function as well

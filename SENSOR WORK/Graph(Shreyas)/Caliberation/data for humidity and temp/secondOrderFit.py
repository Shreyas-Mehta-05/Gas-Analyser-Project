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

df_85 = df_combined[['Temperature', 'Ratio_85%']].copy()
df_85['Humidity'] = 85
df_85 = df_85.rename(columns={'Ratio_85%': 'Rs_Ro'})

# Combine the two datasets
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
H_range = np.linspace(30, 60, 100)  # Covering only 30% and 60% humidity
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



r_squared = model.score(X, y)
print("R-squared:", r_squared)

n = X.shape[0]
p = X.shape[1]
adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
print("Adjusted R-squared:", adjusted_r_squared)


y_pred = model.predict(X)
mse = mean_squared_error(y, y_pred)
print("Mean Squared Error:", mse)
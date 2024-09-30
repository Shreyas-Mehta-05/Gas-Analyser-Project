import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import mean_squared_error



# Load the data from the CSV file
df_combined = pd.read_csv('merge.csv')

# Create separate dataframes for 33% and 85% humidity
df_33 = pd.DataFrame({
    'Temperature': df_combined['Temperature'],
    'Humidity': 33,  # Assign 30% humidity
    'Rs_Ro': df_combined['Ratio_33%']
})

df_85 = pd.DataFrame({
    'Temperature': df_combined['Temperature'],
    'Humidity': 85,  # Assign 60% humidity
    'Rs_Ro': df_combined['Ratio_85%']
})

# Combine both dataframes
df_final = pd.concat([df_33, df_85], ignore_index=True)

# Check for NaN or infinite values
print("Checking for NaN values:")
print(df_final.isna().sum())

print("\nChecking for infinite values:")
print(np.isinf(df_final).sum())

# Replace inf values with NaN and drop rows with NaN
df_final = df_final.replace([np.inf, -np.inf], np.nan).dropna()

# Ensure data types are numeric
df_final['Temperature'] = pd.to_numeric(df_final['Temperature'], errors='coerce')
df_final['Humidity'] = pd.to_numeric(df_final['Humidity'], errors='coerce')
df_final['Rs_Ro'] = pd.to_numeric(df_final['Rs_Ro'], errors='coerce')

# Prepare the features and target
X = df_final[['Temperature', 'Humidity']]
y = df_final['Rs_Ro']

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Print the coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# For visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot of the actual data
ax.scatter(df_final['Temperature'], df_final['Humidity'], df_final['Rs_Ro'], color='r', label='Data Points')

# Generate grid for predictions
T_range = np.linspace(-10, 50, 100)
H_range = np.linspace(33, 85, 100)  # Covering only 33% and 85%
T_grid, H_grid = np.meshgrid(T_range, H_range)

# Predict Rs/R0 over the grid using a DataFrame to avoid warnings
grid_data = pd.DataFrame({'Temperature': T_grid.flatten(), 'Humidity': H_grid.flatten()})
Z = model.predict(grid_data)

# Reshape Z back into the grid shape for plotting
Z = Z.reshape(T_grid.shape)

# Plot the surface
ax.plot_surface(T_grid, H_grid, Z, alpha=0.5)

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Humidity (%)')
ax.set_zlabel('Rs/R0')
ax.set_title('Surface Fit of Rs/R0 Based on Temperature and Humidity')
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
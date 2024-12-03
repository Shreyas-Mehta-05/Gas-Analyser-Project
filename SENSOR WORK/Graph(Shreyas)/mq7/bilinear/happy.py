import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the actual function
def actual_function(H, T):
    return np.sin(H) * np.cos(T)

# Define the bilinear interpolation function
def bilinear_interpolation(H, T, points):
    (H1, T1, R11), (H1, T2, R12), (H2, T1, R21), (H2, T2, R22) = points
    
    return (R11 * (H2 - H) * (T2 - T) +
            R12 * (H2 - H) * (T - T1) +
            R21 * (H - H1) * (T2 - T) +
            R22 * (H - H1) * (T - T1)) / ((H2 - H1) * (T2 - T1))

# Generate grid points
H = np.linspace(-1.5, 1.5, 100)
T = np.linspace(-1.5, 1.5, 100)
H, T = np.meshgrid(H, T)

# Compute actual function values
Z_actual = actual_function(H, T)

# Define example points for bilinear interpolation
# Example data points (H, T, R)
points = [
    (0, 0, actual_function(0, 0)),    # R11
    (0, 1, actual_function(0, 1)),    # R12
    (1, 0, actual_function(1, 0)),    # R21
    (1, 1, actual_function(1, 1))     # R22
]

# Compute bilinear interpolation using the defined points
Z_interpolated = bilinear_interpolation(H, T, points)

# Calculate error
Z_error = Z_actual - Z_interpolated

# Plotting the actual function separately
plt.figure(figsize=(10, 6))
ax1 = plt.axes(projection='3d')
ax1.plot_surface(H, T, Z_actual, cmap='viridis', edgecolor='none')
ax1.set_title('Actual Function $R(H, T) = \sin(H) \cdot \cos(T)$')
ax1.set_xlabel('H')
ax1.set_ylabel('T')
ax1.set_zlabel('R(H, T)')
plt.savefig('actual_function.png')  # Save the actual function plot
plt.show()

# Plotting the interpolated surface separately
plt.figure(figsize=(10, 6))
ax2 = plt.axes(projection='3d')
ax2.plot_surface(H, T, Z_interpolated, cmap='plasma', edgecolor='none')
ax2.set_title('Bilinear Interpolation Surface')
ax2.set_xlabel('H')
ax2.set_ylabel('T')
ax2.set_zlabel('R(H, T)')
plt.savefig('interpolated_surface.png')  # Save the interpolated surface plot
plt.show()

# Plotting the error surface separately
plt.figure(figsize=(10, 6))
ax3 = plt.axes(projection='3d')
ax3.plot_surface(H, T, Z_error, cmap='coolwarm', edgecolor='none')
ax3.set_title('Error Surface')
ax3.set_xlabel('H')
ax3.set_ylabel('T')
ax3.set_zlabel('Error')
plt.savefig('error_surface.png')  # Save the error surface plot
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(T, H):
    a = 1.8086749555143973
    b1 = -1.68368587e-02
    b2 = 2.21726914e-05
    b3 = -8.66430074e-03
    b4 = 1.09457783e-05
    b5 = 6.67479877e-05
    
    return (a + b1*T + b2*T**2 + b3*H + b4*H**2 + b5*T*H)


# Create a grid of temperature (T) and humidity (H) values
T = np.linspace(-10, 50, 100)
H = np.linspace(20, 90, 100)
T, H = np.meshgrid(T, H)

# Compute the values of f(T, H) on the grid
Z = f(T, H)

# Create the figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface #instead of viridis, you can use other color maps like 'coolwarm', 'plasma', 'inferno', 'magma', 'cividis'
# surf = ax.plot_surface(T, H, Z, cmap='plasma', edgecolor='none', alpha=0.5)
surf = ax.plot_surface(T, H, Z, cmap='coolwarm', edgecolor='none', alpha=0.3)
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)


# ax.plot_surface(T, H, Z, color='yellow', alpha=.4)

# Mark the vertical lines (similar to axvlines in 2D)
# T_lines = [5, 10, 15, 20, 25, 30, 35, 40, 45]
# for t in T_lines:
#     ax.plot([t, t], [20, 90], [f(t, 33), f(t, 85)], color='k', linestyle='--', alpha=0.5)

# Plot the red points at T = 20 and T = 25 for both H = 33 and H = 85
T_points = [20, 25]
H1, H2 = 30, 85
for t in T_points:
    ax.scatter(t, H1, f(t, H1), color='r', s=30)
    ax.scatter(t, H2, f(t, H2), color='r', s=30)

T_points = [5, 10, 15, 30, 35, 40, 45]
H1, H2 = 30, 85
for t in T_points:
    ax.scatter(t, H1, f(t, H1), color='k', s=20)
    ax.scatter(t, H2, f(t, H2), color='k', s=20)

# Highlight the point at (T=22, H=59)
T_actual, H_actual = 22, 59
Z_actual = f(T_actual, H_actual)
ax.scatter(T_actual, H_actual, Z_actual, color='b', s=40, label='Actual Value')

# replot the surface just between the 4 points
T = np.linspace(20, 25, 100)
H = np.linspace(30, 85, 100)
T, H = np.meshgrid(T, H)
Z = f(T, H)
# make color to be a shade of light blue
ax.plot_surface(T, H, Z,color='red', alpha=1)
# mark the region between the 4 points with green color
# redraw a green surface between the 4 points
ax.plot([20, 25], [H1, H1], [f(20, H1), f(25, H1)], color='g', alpha=0.5)
ax.plot([20, 25], [H2, H2], [f(20, H2), f(25, H2)], color='g', alpha=0.5)
ax.plot([20, 20], [H1, H2], [f(20, H1), f(20, H2)], color='g', alpha=0.5)
ax.plot([25, 25], [H1, H2], [f(25, H1), f(25, H2)], color='g', alpha=0.5)

# Define the corner points of the rectangular plane
T_rect = [20, 20, 25, 25]
H_rect = [30, 85, 30, 85]
Z_rect = [f(20, 30), f(20, 85), f(25, 30), f(25, 85)]

# Plot the rectangular plane
ax.plot_trisurf(T_rect, H_rect, Z_rect, color='green', alpha=0.4)



# Draw the line parallel to the y-axis
ax.plot([T_actual, T_actual], [H1, H2], [f(T_actual, H1), f(T_actual, H2)], color='k', linestyle='--', alpha=0.7)

# Draw the line parallel to the x-axis (Temperature)
ax.plot([20, 25], [H_actual, H_actual], [Z_actual, Z_actual], color='k', linestyle='--', alpha=0.7)

# Calculate interpolation point
a = (H_actual - H1) / (H2 - H1)
b = (T_actual - 20) / (25 - 20)
calculated = a*b*f(25, 85) + a*(1-b)*f(20, 85) + (1-a)*b*f(25, 30) + (1-a)*(1-b)*f(20, 30)

# Plot the interpolated value as a red star
ax.scatter(T_actual, H_actual, calculated, color='r', marker='*', s=40, label='Interpolated Value')

# Annotate the values of a and b on the plot with better positioning
x_offset, y_offset, z_offset = 1.5, 3, 0.01

ax.text(T_actual + x_offset, (H1 + H_actual) / 2, (Z_actual + f(T_actual, H1)) / 2, 'a', color='k', fontsize=12, zorder=5)
ax.text(T_actual + x_offset, (H2 + H_actual) / 2, (Z_actual + f(T_actual, H2)) / 2, '1-a', color='k', fontsize=12, zorder=5)
ax.text((T_actual + 20) / 2, H_actual + y_offset, Z_actual + z_offset, 'b', fontsize=10, zorder=5)
ax.text((T_actual + 25) / 2, H_actual + y_offset, Z_actual + z_offset, '1-b', fontsize=10, zorder=5)

# Add a label for the calculated error with better positioning
error = Z_actual - calculated
# ax.text(46, 75, np.max(Z) + 0.02, f'Error = {error:.5f}', fontsize=12)
print(f'Error = {error:.5f}')

ax.grid(False)
# Labels and title
ax.set_xlabel('Temperature (°C)', labelpad=15)
ax.set_ylabel('Humidity (%)', labelpad=15)
ax.set_zlabel('Rs/Ro', labelpad=10)
ax.set_title('3D Plot of Rs/Ro vs Temperature and Humidity for MQ2')
plt.legend()
plt.savefig('3dMQ2.png')
plt.show()


# now just make the red surface and green surface to be  again without the black dots
# also remove the black lines
# also remove the text
# also remove the error
# also remove the grid
# also remove the color bar
# also remove the legend
# also remove the title
# also remove the labels
# also remove the surface


# Create the figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')


# replot the surface just between the 4 points
T = np.linspace(20, 25, 100)
H = np.linspace(30, 85, 100)
T, H = np.meshgrid(T, H)
Z = f(T, H)
# make color to be a shade of light blue
#plot the red points at T = 20 and T = 25 for both H = 33 and H = 85
T_points = [20, 25]
H1, H2 = 30, 85
for t in T_points:
    ax.scatter(t, H1, f(t, H1), color='r', s=30)
    ax.scatter(t, H2, f(t, H2), color='r', s=30)

ax.plot_surface(T, H, Z,color='red', alpha=.5)
# mark the actual point with a blue dot
T_actual, H_actual = 22, 59
Z_actual = f(T_actual, H_actual)
plt.plot(22, 59, Z_actual, 'bo',label='Actual Value')

# plot the interpolated value with a red star
a = (H_actual - H1) / (H2 - H1)
b = (T_actual - 20) / (25 - 20)
calculated = a*b*f(25, 85) + a*(1-b)*f(20, 85) + (1-a)*b*f(25, 30) + (1-a)*(1-b)*f(20, 30)
plt.plot(22,59,calculated, 'r*', markersize=10, label='Interpolated Value')


# make a projection of the green surface on the plane surface using the rectangular plane
# replot the surface just between the 4 points
T_rect = [20, 20, 25, 25]
H_rect = [30, 85, 30, 85]
Z_rect = [0.825, 0.825, 0.825, 0.825]

# Plot the rectangular plane
ax.plot_trisurf(T_rect, H_rect, Z_rect, color='green', alpha=0.1)
ax.plot([20, 25], [H1, H1], [0.825, 0.825], color='g', alpha=0.5)
ax.plot([20, 25], [H2, H2], [0.825, 0.825], color='g', alpha=0.5)
ax.plot([20, 20], [H1, H2], [0.825, 0.825], color='g', alpha=0.5)
ax.plot([25, 25], [H1, H2], [0.825, 0.825], color='g', alpha=0.5)
# plot t_actual and h_actual with a black dot on this plane
ax.plot(22, 59, 0.825, 'ko')
# plot the line parallel to y-axis
ax.plot([22, 22], [H1, H2], [0.825, 0.825], 'k--',alpha=0.5)
# plot the line parallel to x-axis
ax.plot([20, 25], [59, 59], [0.825, 0.825], 'k--',alpha=0.5)
# write a and 1-a on the plot
ax.text(22 * 1.01, (H1 + H_actual) / 2, 0.825, 'a', fontsize=12)
ax.text(22 * 1.01, (H_actual + H2) / 2, 0.825, '1-a', fontsize=12)

# Write 'b' and '1-b' on the plot with correct x, y, and z coordinates
ax.text((22 + 20) / 2, 59 * 1.01, 0.825, 'b', fontsize=12)
ax.text((22 + 25) / 2, 59 * 1.01, 0.825, '1-b', fontsize=12)

# to beautify the plot, remove the grid
ax.grid(False)

# mark the region between the 4 points with green color
# redraw a green surface between the 4 points
ax.plot([20, 25], [H1, H1], [f(20, H1), f(25, H1)], color='g', alpha=0.5)
ax.plot([20, 25], [H2, H2], [f(20, H2), f(25, H2)], color='g', alpha=0.5)
ax.plot([20, 20], [H1, H2], [f(20, H1), f(20, H2)], color='g', alpha=0.5)
ax.plot([25, 25], [H1, H2], [f(25, H1), f(25, H2)], color='g', alpha=0.5)
# plot the 4 corner points of the rectangular plane
plt.plot(20, 30, .825, 'ro')
plt.plot(25, 30, .825, 'ro')
plt.plot(20, 85, .825, 'ro')
plt.plot(25, 85, .825, 'ro')

ax.plot([20, 20], [30, 30], [0.825, f(20,30)], color='g', alpha=0.5, linestyle='--')
ax.plot([25, 25], [30, 30], [0.825, f(25,30)], color='g', alpha=0.5, linestyle='--')
ax.plot([20, 20], [85, 85], [0.825, f(20,85)], color='g', alpha=0.5, linestyle='--')
ax.plot([25, 25], [85, 85], [0.825, f(25,85)], color='g', alpha=0.5, linestyle='--')

ax.plot([T_actual, T_actual], [H_actual, H_actual], [calculated, 0.825], color='k', linestyle='--', alpha=0.7)

# Define the corner points of the rectangular plane
T_rect = [20, 20, 25, 25]
H_rect = [30, 85, 30, 85]
Z_rect = [f(20, 30), f(20, 85), f(25, 30), f(25, 85)]
# use diff marker for below points
ax.plot([T_actual,T_actual],[H_actual,H_actual],[calculated,Z_actual],'b',alpha=1,label='Error')    

# Plot the rectangular plane
ax.plot_trisurf(T_rect, H_rect, Z_rect, color='green', alpha=0.4)
plt.legend()
# name the axes
ax.set_xlabel('Temperature (°C)', labelpad=15)
ax.set_ylabel('Humidity (%)', labelpad=15)
ax.set_zlabel('Rs/Ro', labelpad=10)
# show the plot
ax.view_init(30, 30)
ax.set_title('Error Calculation for Bilinear Interpolation for MQ2')

plt.savefig('3dErrorMQ2.png')
plt.show()
# plot
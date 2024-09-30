import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Remove old variables (not necessary in Python, but included for completeness)
# xlim, ylim, minppm, maxppm, mres, mppm, pointsdata all initialized below

# Set input values
xlim = [100-1, 10000+10000]
ylim = [0.1, 10]
minppm = 20
maxppm = 2000
mres = 250000
mppm = 10
pointsdata = """
199.2355955077503, 5.179818678510565
494.2980661327712, 4.023927177278145
795.3740813598098, 3.4087291628485135
1012.5136053893372, 3.1498543904211624
1496.1928685611476, 2.7322089102327425
1987.4991375337347, 2.524897569620085
3000.1200221217523, 2.190196745355461
4931.413657205698, 1.840743119565833
3985.3697881460093, 1.9921244091535069
296.4927294317968, 4.638060001906838
10030.141206670845, 1.4294862139810809
"""

# Load points
points = np.array([list(map(float, line.split(','))) for line in pointsdata.strip().split('\n')])
x = points[:, 0]
y = points[:, 1]

# Define power-law model for nonlinear regression
def power_law(x, a, b):
    return a * np.power(x, b)

# Log-log slope estimation for initial values
xfirst, xlast = x[0], x[-1]
yfirst, ylast = y[0], y[-1]
bstart = np.log(ylast / yfirst) / np.log(xlast / xfirst)
astart = yfirst / (xfirst ** bstart)

# Perform the nonlinear regression (fit)
popt, pcov = curve_fit(power_law, x, y, p0=[astart, bstart])
a, b = popt

# Reverse axis data for reversed fit
pointsrev = points[:, [1, 0]]  # Swap columns (x <-> y)
xrev = pointsrev[:, 0]
yrev = pointsrev[:, 1]

# Perform the nonlinear regression on the reversed data
popt_rev, _ = curve_fit(power_law, xrev, yrev, p0=[astart, bstart])
a_rev, b_rev = popt_rev

# Plot fit curve (log-log scale)
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'bo', label='Data points')
x_fit = np.linspace(min(x), max(x), 100)
y_fit = power_law(x_fit, a, b)
plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {a:.3f} * x ^ {b:.3f}')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('ppm')
plt.ylabel('Rs/Ro')
plt.xlim(xlim)
plt.ylim(ylim)
plt.grid(True, which='both', ls='--')
plt.title('Fit Curve (Log-Log Scale)')
plt.legend()
plt.show()

# Plot reversed fit curve (log-log scale)
plt.figure(figsize=(10, 6))
plt.plot(xrev, yrev, 'bo', label='Reversed Data points')
x_fit_rev = np.linspace(min(xrev), max(xrev), 100)
y_fit_rev = power_law(x_fit_rev, a_rev, b_rev)
plt.plot(x_fit_rev, y_fit_rev, 'r-', label=f'Reversed Fit: y = {a_rev:.3f} * x ^ {b_rev:.3f}')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Rs/Ro')
plt.ylabel('ppm')
plt.xlim(ylim)
plt.ylim(xlim)
plt.grid(True, which='both', ls='--')
plt.title('Reversed Fit Curve (Log-Log Scale)')
plt.legend()
plt.show()

# Plot fit curve (linear scale)
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'bo', label='Data points')
plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {a:.3f} * x ^ {b:.3f}')
plt.xlabel('ppm')
plt.ylabel('Rs/Ro')
plt.grid(True)
plt.title('Fit Curve (Linear Scale)')
plt.legend()
plt.show()

# Plot reversed fit curve (linear scale)
plt.figure(figsize=(10, 6))
plt.plot(xrev, yrev, 'bo', label='Reversed Data points')
plt.plot(x_fit_rev, y_fit_rev, 'r-', label=f'Reversed Fit: y = {a_rev:.3f} * x ^ {b_rev:.3f}')
plt.xlabel('Rs/Ro')
plt.ylabel('ppm')
plt.grid(True)
plt.title('Reversed Fit Curve (Linear Scale)')
plt.legend()
plt.show()

# Output correlation function coefficients
print("\nCorrelation function coefficients")
print(f"Estimated a: {a_rev}")
print(f"Estimated b: {b_rev}\n")

# Estimate min Rs/Ro if minppm is set
if minppm != 0:
    minRsRo = (maxppm / a_rev) ** (1 / b_rev)
    print(f"Estimated min Rs/Ro: {minRsRo}")

# Estimate max Rs/Ro if maxppm is set
if maxppm != 0:
    maxRsRo = (minppm / a_rev) ** (1 / b_rev)
    print(f"Estimated max Rs/Ro: {maxRsRo}")

# Estimate Ro if mppm and mres are set
if mppm != 0 and mres != 0:
    Ro = mres * (a_rev / mppm) ** (1 / b_rev)
    print(f"Estimated Ro: {Ro}")

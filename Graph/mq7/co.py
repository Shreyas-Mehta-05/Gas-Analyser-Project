import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Remove old variables (not necessary in Python, but included for completeness)
# xlim, ylim, minppm, maxppm, mres, mppm, pointsdata all initialized below

# Set input values
xlim = [10, 10000]
ylim = [0.01, 100]
minppm = 10
maxppm = 10000
mres = 15000
mppm = 8
pointsdata = """
49.90511093135102, 1.6273501612935244
61.54707525675475, 1.3940959089311384
70.78083520755492, 1.2793549399264523
80.45720176870928, 1.1740235707644142
99.22641909399708, 1.0057463328546579
140.73365807741018, 0.8044316206284229
165.66252758980187, 0.7132331516133246
197.2920621248877, 0.6215783855925411
273.3771590400109, 0.4971315388998798
401.5225579493524, 0.3908582208354385
512.8016451279926, 0.3406900297990933
603.6368118661717, 0.3020659773257298
710.5620742480455, 0.27248012918018966
807.7021980501505, 0.2543965627600148
1019.6044052793735, 0.22173731315984377
2051.0347500566722, 0.14432141195069043
3012.456205842839, 0.11346938564456233
4078.07597032357, 0.0923250366914805
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

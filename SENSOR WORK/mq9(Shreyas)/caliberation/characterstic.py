import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Remove old variables (not necessary in Python, but included for completeness)
# xlim, ylim, minppm, maxppm, mres, mppm, pointsdata all initialized below

# Set input values
xlim = [100, 10000+1000] # ppm
ylim = [0.1, 10] # Rs/Ro
minppm = 500
maxppm = 10000
mres = 15033.893448275863
mppm = 8
pointsdata = """
200.03654747059682, 2.056330793557282
303.2319511315635, 1.6966861629080394
400.14620323956257, 1.4882487341249948
501.7361994709734, 1.3518540026851549
606.5747258713063, 1.2279595491477746
701.9008248382728, 1.1652353789683834
812.2078729887168, 1.1057151592183228
1011.0074553350253, 0.9956402995308042
1499.3784064181998, 0.8287166645623056
2007.678352461578, 0.7143152846169966
2499.0865636211283, 0.6432046065446696
3021.2744243996826, 0.5893841901121226
4016.090460578697, 0.5124805876960934
4999.086480169275, 0.4614627208314444
5999.70576547629, 0.42284963325319186
7044.668134006179, 0.39429877420790665
7975.2308815164915, 0.3644767494653629
9094.850458504758, 0.33986723468534547
10000, 0.331073254995991
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
plt.savefig('mq9_characterstic_1.png')
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
plt.savefig('mq9_characterstic_2.png')
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
plt.savefig('mq9_characterstic_3.png')
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
plt.savefig('mq9_characterstic_4.png')
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

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Remove old variables (not necessary in Python, but included for completeness)
# xlim, ylim, minppm, maxppm, mres, mppm, pointsdata all initialized below

# Set input values
xlim = [0.01, 1000] # ppm
ylim = [0.001, 10] # Rs/Ro
minppm = 1
maxppm = 200
mres = 15033.893448275863
mppm = 8
pointsdata = """
1.0090885378417724, 0.5782370066191735
2.0070307549896858, 0.49086666210417085
3.015583207921911, 0.43864776634302116
3.991891990062515, 0.4001290165998865
5.005075223132971, 0.3763153719622981
6.052368242529728, 0.3612010990665549
8.011849994652449, 0.33966363004551164
9.954864738974841, 0.3227118403863827
19.979719692884874, 0.2630526944554832
30.292558331962407, 0.23746071493922785
49.37609038870656, 0.20580238516300275
69.00805763736759, 0.1858135211327176
144.9106139539427, 0.15144742508513367
99.09933197128464, 0.1694663769318376
197.10401972328057, 0.14240850033864239
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
plt.savefig('mq136_characterstic_1.png')
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
plt.savefig('mq136_characterstic_2.png')
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
plt.savefig('mq136_characterstic_3.png')
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
plt.savefig('mq136_characterstic_4.png')
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

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Remove old variables (not necessary in Python, but included for completeness)
# xlim, ylim, minppm, maxppm, mres, mppm, pointsdata all initialized below

# Set input values
xlim = [0.01, 100000] # ppm
ylim = [.11,1] # Rs/Ro
minppm = 5
maxppm = 5000
mres = 15033.893448275863
mppm = 8
pointsdata = """
1.045800744138103, 0.7584065017590683
1.9576461640127947, 0.6652499663347582
2.88596948140514, 0.6075633160707784
5.01374306822658, 0.5383427435831706
7.281764492776178, 0.46287978165948546
9.962750503745998, 0.40405634660838996
11.917222297522786, 0.3690610030292662
13.63081677502173, 0.34568618961148506
16.550100993040186, 0.31574371593677675
19.796865585096565, 0.2869508626557279
30.069065781101312, 0.2517328489277533
39.33812121933796, 0.23107783478085278
49.95067127862733, 0.21319016796829118
70.41252508476667, 0.1898748483472156
99.25639759989119, 0.16826132407456496
120.51393776297992, 0.15602249075333613
146.32416193145502, 0.14250821259459714
203.20839850331072, 0.13549646952462543
258.0295042078778, 0.1307939081312089
363.72902450704396, 0.12435752340583714
497.64607544359575, 0.11764684461249969
701.5024197582875, 0.11528299956359486
1003.7388767529611, 0.112965730111953
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
plt.savefig('sen0564_characterstic_1.png')
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
plt.savefig('sen0564_characterstic_2.png')
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
plt.savefig('sen0564_characterstic_3.png')
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
plt.savefig('sen0564_characterstic_4.png')
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

import numpy as np


# General Equation: Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH
def calculate_rs_ro_sen0564(T, H):
    # Coefficients and intercept
    a = 1.7901285236777154
    b1 = -0.020923638050983233
    b2 = -1.6076406512106393e-05
    b3 = -0.012004842116623383
    b4 = 1.3977402911589597e-05
    b5 = 8.30860122e-05
    """
    Calculate Rs/Ro based on temperature (T) and humidity (H).

    Parameters:
    T : float or np.array
        Temperature in degrees Celsius.
    H : float or np.array
        Humidity in percentage.

    Returns:
    Rs/Ro : float or np.array
        The calculated Rs/Ro value.
    """
    rs_ro = a + b1 * T + b2 * T**2 + b3 * H + b4 * H**2 + b5 * T * H
    return rs_ro



# Path: Gas-Analyser-Project/SEN0564/formula/lookup_table.py
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Data points from the lookup table
pointsdata = """
1.045800744138103, 0.7584065017590683
5.01374306822658, 0.5383427435831706
9.962750503745998, 0.40405634660838996
19.796865585096565, 0.2869508626557279
49.95067127862733, 0.21319016796829118
99.25639759989119, 0.16826132407456496
146.32416193145502, 0.14250821259459714
497.64607544359575, 0.11764684461249969
1003.7388767529611, 0.112965730111953
"""
# Sort the data based on ppm (concentration)
pointsdata = '\n'.join(sorted(pointsdata.strip().split('\n'), key=lambda x: float(x.split(',')[0])))

# Convert data into a NumPy array
points = np.array([list(map(float, line.split(','))) for line in pointsdata.strip().split('\n')])
ppm = points[:, 0]  # Concentration in ppm
rs_ro = points[:, 1]  # Rs/Ro values

# Function to logarithmically interpolate for a given Rs/Ro value
def interpolate_log_rs_ro_sen0564(rs_ro_value, rs_ro):
    """
    Interpolates ppm values for a given Rs/Ro value using logarithmic interpolation.
    """
    # Check if Rs/Ro is outside the bounds
    if rs_ro_value < min(rs_ro) or rs_ro_value > max(rs_ro):
        raise ValueError(f"Rs/Ro value {rs_ro_value} is out of bounds.")
    
    # Find the two closest Rs/Ro points (R1, R2)
    for i in range(len(rs_ro) - 1):
        if rs_ro[i] >= rs_ro_value >= rs_ro[i + 1]:
            # Perform logarithmic interpolation
            log_r1, log_r2 = np.log(rs_ro[i]), np.log(rs_ro[i + 1])
            log_ppm1, log_ppm2 = np.log(ppm[i]), np.log(ppm[i + 1])
            log_ppm_value = log_ppm1 + (log_ppm2 - log_ppm1) * (np.log(rs_ro_value) - log_r1) / (log_r2 - log_r1)
            return np.exp(log_ppm_value)  # Return the result in original space 


# now we have the lookup table and the interpolation function, we can use them to calculate the concentration of a gas based on the Rs/Ro value
def calculate_concentration_sen0564(rs_ro_value,T,H):
    # Calculate the Rs/Ro value based on temperature and humidity
    # Interpolate the concentration based on the Rs/Ro value
    concentration = interpolate_log_rs_ro_sen0564(rs_ro_value, rs_ro)
    return concentration*calculate_rs_ro_sen0564(20,55)/calculate_rs_ro_sen0564(T,H)
    # return concentration*calculate_rs_ro_sen0564(T,H)/calculate_rs_ro_sen0564(20,55)


pointsData1 = """
1.045800744138103, 0.7584065017590683
5.01374306822658, 0.5383427435831706
9.962750503745998, 0.40405634660838996
19.796865585096565, 0.2869508626557279
49.95067127862733, 0.21319016796829118
99.25639759989119, 0.16826132407456496
146.32416193145502, 0.14250821259459714
497.64607544359575, 0.11764684461249969
1003.7388767529611, 0.112965730111953
"""
points1= np.array([list(map(float, line.split(','))) for line in pointsData1.strip().split('\n')])
ppm1 = points1[:, 0]  # Concentration in ppm
rs_ro1 = points1[:, 1]  # Rs/Ro values

def interpolate_log_ppm_sen0564(ppm_value, ppm):
    """
    Interpolates Rs/Ro values for a given ppm value using logarithmic interpolation.
    
    Parameters:
    ppm_value (float): Ppm value to interpolate.
    ppm (list or np.array): Ppm values from the dataset.
    rs_ro (list or np.array): Corresponding Rs/Ro values for ppm.
    
    Returns:
    float: Interpolated Rs/Ro value.
    """
    # Check if ppm is outside the bounds
    if ppm_value < min(ppm) or ppm_value > max(ppm):
        raise ValueError(f"ppm value {ppm_value} is out of bounds.")
    
    # Find the two closest ppm points (ppm1, ppm2)
    for i in range(len(ppm) - 1):
        if ppm[i] <= ppm_value <= ppm[i + 1]:
            # Perform logarithmic interpolation
            log_ppm1, log_ppm2 = np.log(ppm[i]), np.log(ppm[i + 1])
            log_r1, log_r2 = np.log(rs_ro[i]), np.log(rs_ro[i + 1])
            log_rs_ro_value = log_r1 + (log_r2 - log_r1) * (np.log(ppm_value) - log_ppm1) / (log_ppm2 - log_ppm1)
            return np.exp(log_rs_ro_value)  # Return the result in original space



def calculate_Ro_sen0564(rs_value, T, H, ppm):
    """
    Calculate the Ro value based on the Rs value, temperature, humidity, and ppm (concentration).

    Parameters:
    rs_value : float
        The measured Rs value from the sensor.
    T : float
        Temperature in degrees Celsius.
    H : float
        Humidity in percentage.
    ppm : float
        Concentration of the gas in ppm.

    Returns:
    Ro : float
        The calculated Ro value.
    """
    # Calculate Rs/Ro based on the given temperature and humidity
    rs_ro = interpolate_log_ppm_sen0564(ppm*calculate_rs_ro_sen0564(T, H)/calculate_rs_ro_sen0564(20, 55), ppm1)
    return rs_value / rs_ro


given_Rs = 1000
T = 28
H = 65
given_ppm = 100


print(calculate_Ro_sen0564(given_Rs, T, H, given_ppm))  # Output: 0.000118



print(calculate_Ro_sen0564(1000, 28, 60, 100))  # 0.889
checkRatio = .7
setppm=calculate_concentration_sen0564(checkRatio, T, H)
print("ppm: ",setppm)  # 100.0
print("ratio: ",interpolate_log_ppm_sen0564(setppm*calculate_rs_ro_sen0564(T,H)/calculate_rs_ro_sen0564(20,55),ppm1))  # 0.6
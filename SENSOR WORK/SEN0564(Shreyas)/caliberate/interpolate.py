import numpy as np

# Data points from the lookup table
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
# sort the data on the based
pointsdata = '\n'.join(sorted(pointsdata.strip().split('\n'), key=lambda x: float(x.split(',')[0])))


# Convert data into a NumPy array
points = np.array([list(map(float, line.split(','))) for line in pointsdata.strip().split('\n')])
ppm = points[:, 0]  # Concentration in ppm
rs_ro = points[:, 1]  # Rs/Ro values

# Function to linearly interpolate for a given Rs/Ro value
def interpolate_rs_ro(rs_ro_value, rs_ro, ppm):
    # Check if Rs/Ro is outside the bounds
    if rs_ro_value < min(rs_ro) or rs_ro_value > max(rs_ro):
        raise ValueError(f"Rs/Ro value {rs_ro_value} is out of bounds.")

    # Find the two closest Rs/Ro points (R1, R2)
    for i in range(len(rs_ro) - 1):
        if rs_ro[i] >= rs_ro_value >= rs_ro[i + 1]:
            
            # Perform linear interpolation
            r1, r2 = rs_ro[i], rs_ro[i + 1]
            ppm1, ppm2 = ppm[i], ppm[i + 1]
            ppm_value = ppm1 + (ppm2 - ppm1) * (rs_ro_value - r1) / (r2 - r1)
            return ppm_value

# Example Rs/Ro value to interpolate
rs_ro_value = 0.35  # You can change this value

# Interpolate the ppm for the given Rs/Ro value
try:
    interpolated_ppm = interpolate_rs_ro(rs_ro_value, rs_ro, ppm)
    print(interpolated_ppm)
    print(f"Interpolated ppm for Rs/Ro = {rs_ro_value}: {interpolated_ppm:.3f}")
except ValueError as e:
    print(e)

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
def interpolate_log_rs_ro(rs_ro_value, rs_ro, ppm):
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

# Generate Rs/Ro values for plotting (between min and max)
rs_ro_values = np.logspace(np.log10(min(rs_ro)), np.log10(max(rs_ro)), 1000)

# Interpolate the ppm values for each Rs/Ro
ppm_values = []
for r_value in rs_ro_values:
    try:
        ppm_val = interpolate_log_rs_ro(r_value, rs_ro, ppm)
        ppm_values.append(ppm_val)
    except ValueError:
        pass  # Skip out-of-bound values

# Plot the interpolated ppm vs Rs/Ro values
plt.figure(figsize=(10, 6))
plt.plot(rs_ro_values[:len(ppm_values)], ppm_values, label="Interpolated ppm")
plt.scatter(rs_ro, ppm, color='blue', label='Data points', zorder=5)  # Changed data points to blue
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Rs/Ro')
plt.ylabel('ppm')
plt.title('Interpolated Gas Concentration (ppm) vs Rs/Ro (Log-Log)')
plt.grid(True, which='both', linestyle='--')
plt.legend()
plt.savefig('sen0564_interpolate.png')
plt.show()

# now sort the data based on the ppm
pointsdata = '\n'.join(sorted(pointsdata.strip().split('\n'), key=lambda x: float(x.split(',')[1])))
# now plot the interpolated Rs/RO vs ppm
plt.figure(figsize=(10, 6))
plt.plot(ppm, rs_ro, 'bo', label='Data points')
plt.plot(ppm_values, rs_ro_values[:len(ppm_values)], 'r-', label='Interpolated curve')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('ppm')
plt.ylabel('Rs/Ro')
plt.grid(True, which='both', ls='--')
plt.title('Interpolated Rs/Ro vs ppm (Log-Log Scale)')
plt.legend()
plt.savefig('sen0564_interpolate1.png')
plt.show()




# Concatenate the two images to show the comparison (datasheet.png and sen0564_interpolate.png)
img1 = Image.open('datasheet.png')
img1 = img1.resize((600*2, 400*2))

img2 = Image.open('sen0564_interpolate1.png')
img2 = img2.resize((600*2, 400*2))
# img2 = img2.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)

# Create a new image with twice the width
new_img = Image.new('RGB', (1200*2, 400*2))
new_img.paste(img1, (0, 0))
new_img.paste(img2, (600*2, 0))

# Save the new image
new_img.save('datasheet_interpolate.png')

# Display the new image
new_img.show()

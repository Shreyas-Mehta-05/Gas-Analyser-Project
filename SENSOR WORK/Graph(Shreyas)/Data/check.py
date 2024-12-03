import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO  # Correct import for StringIO

# Load the data from the provided CSV data
data = """
created_at,entry_id,field1,field2,field3,field4
2024-09-16 20:40:01 UTC,113,0.00,0.00,0.00,342.03
2024-09-16 20:40:12 UTC,114,0.00,0.00,0.01,135.24
2024-09-16 20:40:23 UTC,115,0.04,0.14,0.18,71.12
2024-09-16 20:40:34 UTC,116,0.53,1.55,2.05,50.04
2024-09-16 20:40:44 UTC,117,0.24,0.69,0.83,53.67
2024-09-16 20:40:55 UTC,118,0.82,5.51,9.13,36.11
2024-09-16 20:41:06 UTC,119,6.84,19.93,8.80,36.45
2024-09-16 20:41:17 UTC,120,0.04,0.05,0.10,84.41
2024-09-16 20:41:27 UTC,121,0.19,0.60,1.65,50.49
2024-09-16 20:41:38 UTC,122,0.05,0.06,0.12,87.65
"""

# Read the data into a DataFrame
df = pd.read_csv(StringIO(data))

# Convert 'created_at' to datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Replace 'inf' with NaN and drop them for mean calculation (if needed)
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Calculate mean values
mean_values = df[['field1', 'field2', 'field3', 'field4']].mean()

# Output the mean values
print("Mean values:")
print(mean_values)

# Plot the mean values
fields = ['LPG (field1)', 'CO (field2)', 'Smoke (field3)', 'Sensor Resistance (field4)']
mean_values_list = [mean_values['field1'], mean_values['field2'], mean_values['field3'], mean_values['field4']]

plt.figure(figsize=(10, 6))
plt.bar(fields, mean_values_list, color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Field')
plt.ylabel('Mean Value')
plt.title('Mean Values of Gas Sensor Readings and Sensor Resistance')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()

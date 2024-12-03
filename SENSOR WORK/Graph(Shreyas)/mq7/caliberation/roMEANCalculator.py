# created_at,entry_id,field1
# 2024-09-30 12:48:11 UTC,1,14848.30
# 2024-09-30 12:48:21 UTC,2,15231.05
# 2024-09-30 12:48:31 UTC,3,14848.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('1.csv')
df['created_at'] = pd.to_datetime(df['created_at'])
# calculated mean of the field1 of values entry_id greater than 20
mean = df[df['entry_id'] > 10]['field1'].mean()

print(mean)

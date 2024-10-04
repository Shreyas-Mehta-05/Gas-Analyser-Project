# plot

import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes


def f(T, H):
    a = 1.8086749555143973
    b1 = -1.68368587e-02
    b2 = 2.21726914e-05
    b3 = -8.66430074e-03
    b4 = 1.09457783e-05
    b5 = 6.67479877e-05
    
    return (a + b1*T + b2*T**2 + b3*H + b4*H**2 + b5*T*H)
# plot the function at two different Humidity levels 33% and 85%
T = np.linspace(-10, 50, 100)
H1 = 30
H2 = 85
plt.figure(figsize=(10, 6))
# also mark x=20 and x=27 on the plot with red color and - color should be black and

plt.axvline(x=5, color='k', linestyle='--')
plt.axvline(x=10, color='k', linestyle='--')
plt.axvline(x=15, color='k', linestyle='--')
plt.axvline(x=20, color='k', linestyle='--')
plt.axvline(x=25, color='k', linestyle='--')
plt.axvline(x=30, color='k', linestyle='--')
plt.axvline(x=35, color='k', linestyle='--')
plt.axvline(x=40, color='k', linestyle='--')
plt.axvline(x=45, color='k', linestyle='--')
# plot point on curves at T=20 and T=25 i.e. f(20, H1) and f(25, H1) and f(20, H2) and f(25, H2)
plt.plot(T, f(T, H1), label='Humidity = 30%')
plt.plot(T, f(T, H2), label='Humidity = 85%')
plt.plot(T,f(T,59),label='Humidity = 59%',color='green',linestyle='--',alpha=0.3)

plt.plot(20, f(20, H1), 'ro')
plt.plot(25, f(25, H1), 'ro')
plt.plot(20, f(20, H2), 'ro')
plt.plot(25, f(25, H2), 'ro')

plt.plot(15, f(15, H1), 'ko')
plt.plot(15, f(15, H2), 'ko')
plt.plot(10, f(10, H1), 'ko')
plt.plot(10, f(10, H2), 'ko')
T1=[5,10,15,20,25,30,35,40,45]
for i in T1:
    if i==20 or i==25:
        continue
    plt.plot(i, f(i, H1), 'ko')
    plt.plot(i, f(i, H2), 'ko')






# color the region between the 4 points to be green
plt.fill_between([20, 25], [f(20, H1), f(25, H1)], [f(20, H2), f(25, H2)], color='g', alpha=0.2)

# take any arbitray point in this region and mark it with a black dot
plt.plot(22, f(22, 59), 'bo',label='Actual Value')
# now draw a line parallel to y-axis from the point to the curve only in the region
plt.plot([22, 22], [f(22, H1), f(22, H2)], 'k--',alpha=0.5)
# now draw a line parallel to x-axis from the point to the curve only in the region
plt.plot([20, 25], [f(22, 59), f(22, 59)], 'k--',alpha=0.5)
# calculate a and b
# a = H-H1/(H2-H1)
# b = T-T1/(T2-T1)
a = (59-H1)/(H2-H1)
b = (22-20)/(25-20)
print(a, b)
# write a and 1-a on the plot
plt.text(22*1.01, (f(22, 59)+f(22,40))/2, 'a', fontsize=12)
plt.text(22*1.01, (f(22, 59)+f(22,85))/2, '1-a', fontsize=12)
# write b and 1-b on the plot 
plt.text((22+19)/2, f(22, 59)*1.01, 'b', fontsize=10)
plt.text((22+24)/2, f(22, 59)*1.01, '1-b', fontsize=10)

# also write values of a and b on the plot at the end of the graph plot it like a label
a=round(a,3)
plt.text(46, 1.18+.3, 'a = (H-H1)/(H2-H1)\n   = '+str(a), fontsize=10)
plt.text(46, 1.14+.2, 'b = (T-T1)/(T2-T1)\n   = '+str(b), fontsize=10)

# now calculate point of interpolation
calculated = a*b*f(25, 85) + a*(1-b)*f(20, 85) + (1-a)*b*f(25, 33) + (1-a)*(1-b)*f(20, 33)
# mark this point with a red star and label it as interpolated value
plt.plot(22, calculated, 'r*', markersize=10, label='Interpolated Value')
# calculate the error
error = f(22, 59) - calculated
# write the error on the plot
# plt.text(46, 1.12, 'Error = '+str(error), fontsize=10)


plt.xlabel('Temperature (°C)')
plt.ylabel('Rs/Ro')
plt.title('Rs/Ro vs Temperature at Different Humidity Levels for MQ2')
plt.legend()
# plt.grid()
plt.savefig('2dMQ2.png')
plt.show()
# plot





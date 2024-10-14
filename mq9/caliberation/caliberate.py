def f_mq9(T,h):
    # Coefficients from your regression
    a = 1.2636396581018856
    b1 = -0.015411273502357305
    b2 = 0.0001423447717815803
    b3 = -2.667160028389554e-07
    b4 = -3.147248816276855e-05
    b5 = 3.5955470516473796e-05
    
    # Evaluate the equation
    Rs_Ro = a + b1*T + b2*(T**2) + b3*h + b4*(h**2) + b5*T*h
    
    return Rs_Ro

def getRatio_mq9(ppm):
    return 23.743*(ppm**(-0.461))

currentHumidity = 32
currentTemperature = 67
currentPpm = 0.4
meanRs=5400
experimentVal = getRatio_mq9(currentPpm)*f_mq9(currentTemperature,currentHumidity)/f_mq9(20,65)
calculatedRo=meanRs/experimentVal
print("Calculated Ro_mq9: ", calculatedRo)

# lpg value is arounf 0.4

def formula_mq9(H,T,Rs_mq9,Ro_mq9=2962.049073305054):
    return  (963.40351*(Rs_mq9/Ro_mq9)**(-2.16919739696))*(f_mq9(20,65)/f_mq9(T,H))**(-2.16919739696)

print(formula_mq9(currentHumidity,currentTemperature,meanRs, calculatedRo))
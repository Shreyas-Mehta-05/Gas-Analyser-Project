def f_mq136(T,h):
    # Coefficients from your regression
    a = 1.8049213062479526
    b1 = -0.01676578961983332
    b2 = 2.2683055653041216e-05
    b3 = -0.008472631405786416
    b4 = 8.707501494816326e-06
    b5 = 6.712560534401002e-05
    
    # Evaluate the equation
    Rs_Ro = a + b1*T + b2*(T**2) + b3*h + b4*(h**2) + b5*T*h
    
    return Rs_Ro

def getRatio_mq136(ppm):
    return 0.585*(ppm**(-0.267))

currentHumidity = 32
currentTemperature = 67
currentPpm = 2.8
experimentVal = getRatio_mq136(currentPpm)*f_mq136(currentTemperature,currentHumidity)/f_mq136(20,65)
meanRs=5400
calculatedRo=meanRs/experimentVal
print("Calculated Ro_136: ", calculatedRo)

def formula_mq136(H,T,Rs_mq136,Ro_mq136=2962.049073305054):
    return  (0.1342531*(Rs_mq136/Ro_mq136)**(-3.74531835206))*(f_mq136(20,65)/f_mq136(T,H))**(-3.74531835206)

print(formula_mq136(currentHumidity,currentTemperature,meanRs, calculatedRo))

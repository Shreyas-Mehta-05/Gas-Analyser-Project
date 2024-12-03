print("General Equation: Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH")
# Estimated a: 1.2094342542500245
# Estimated b1: -0.01094546624860255
# Estimated b2: 8.559231727624334e-05
# Estimated b3: -2.220918787838429e-07
# Estimated b4: -2.6206841578149175e-05
# Estimated b5: 1.4963577356169694e-05


def f_mq7(T, H):
    a = 1.2094342542500245
    b1 = -0.01094546624860255
    b2 = 8.559231727624334e-05
    b3 = -2.220918787838429e-07
    b4 = -2.6206841578149175e-05
    b5 = 1.4963577356169694e-05
    return (a + b1*T + b2*T**2 + b3*H + b4*H**2 + b5*T*H)



def getRatio_mq7(ppm):
    a = 22.679
    b = -.676
    return a * (ppm**b)
currentHumidity = 32
currentTemperature = 67
currentPpm = 2.8
experimentVal = getRatio_mq7(currentPpm)*f_mq7(currentTemperature,currentHumidity)/f_mq7(20,65)
meanRs=15033.893448275863
meanRs=5400
calculatedRo=meanRs/experimentVal
print("Calculated Ro_mq7: ", calculatedRo)




# Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH
def formula_mq7(H,T,Rs,Ro=2962.049073305054):
    return  (101.24201*(Rs/Ro)**(-1.4792899))*(f_mq7(20,65)/f_mq7(T,H))**(-1.4792899)

print(formula_mq7(currentHumidity,currentTemperature,meanRs, calculatedRo))


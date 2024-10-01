print("General Equation: Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH")
# Estimated a: 1.2094342542500245
# Estimated b1: -0.01094546624860255
# Estimated b2: 8.559231727624334e-05
# Estimated b3: -2.220918787838429e-07
# Estimated b4: -2.6206841578149175e-05
# Estimated b5: 1.4963577356169694e-05


def f(T, H):
    a = 1.2094342542500245
    b1 = -0.01094546624860255
    b2 = 8.559231727624334e-05
    b3 = -2.220918787838429e-07
    b4 = -2.6206841578149175e-05
    b5 = 1.4963577356169694e-05
    return (a + b1*T + b2*T**2 + b3*H + b4*H**2 + b5*T*H)


# a * ppm^b = Rs/Ro
# Estimated a: 93.24613464596311
# Estimated b: -1.5895193211019845

def getRatio(ppm):
    a = 22.679
    b = -.676
    return a * (ppm**b)

experimentVal = getRatio(8)*f(27,77)/f(20,65)
meanRs=15033.893448275863
meanRs=4000.893448275863
calculatedRo=meanRs/experimentVal
print("Calculated Ro: ", calculatedRo)




# Rs/Ro = a + b1*T + b2*T^2 + b3*H + b4*H^2 + b5*TH
def formula(H,T,Rs,Ro=2962.049073305054):
    return  (101.24201*(Rs/Ro)**(-1.4792899))*(f(20,65)/f(T,H))**(-1.4792899)
    # return  (93.24613464596311*(Rs/Ro)**(-1.5895193211019845))*(f(20,65)/f(T,H))**(-1.5895193211019845)

print(formula(75,31.8,meanRs, 1000.6921305109535))

print(formula(75,31.8,100, 1000.6921305109535))

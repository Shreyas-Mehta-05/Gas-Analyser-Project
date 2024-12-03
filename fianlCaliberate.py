# General utility functions for gas sensors

def f_mq9(T, H):
    # Coefficients from regression for MQ9
    a = 1.2636396581018856
    b1 = -0.015411273502357305
    b2 = 0.0001423447717815803
    b3 = -2.667160028389554e-07
    b4 = -3.147248816276855e-05
    b5 = 3.5955470516473796e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq9(ppm):
    return 23.743*(ppm**(-0.461))

def formula_mq9(H, T, Rs_mq9, Ro_mq9=2962.049073305054):
    return (963.40351 * (Rs_mq9 / Ro_mq9)**(-2.16919739696)) * (f_mq9(20, 65) / f_mq9(T, H))**(-2.16919739696)

# MQ7 functions
def f_mq7(T, H):
    # Coefficients from regression for MQ7
    a = 1.2094342542500245
    b1 = -0.01094546624860255
    b2 = 8.559231727624334e-05
    b3 = -2.220918787838429e-07
    b4 = -2.6206841578149175e-05
    b5 = 1.4963577356169694e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq7(ppm):
    a = 22.679
    b = -0.676
    return a * (ppm**b)

def formula_mq7(H, T, Rs, Ro=2962.049073305054):
    return (101.24201 * (Rs / Ro)**(-1.4792899)) * (f_mq7(20, 65) / f_mq7(T, H))**(-1.4792899)

# MQ136 functions
def f_mq136(T, H):
    # Coefficients from regression for MQ136
    a = 1.8049213062479526
    b1 = -0.01676578961983332
    b2 = 2.2683055653041216e-05
    b3 = -0.008472631405786416
    b4 = 8.707501494816326e-06
    b5 = 6.712560534401002e-05
    return a + b1*T + b2*(T**2) + b3*H + b4*(H**2) + b5*T*H

def getRatio_mq136(ppm):
    return 0.585 * (ppm**(-0.267))

def formula_mq136(H, T, Rs_mq136, Ro_mq136=2962.049073305054):
    return (0.1342531 * (Rs_mq136 / Ro_mq136)**(-3.74531835206)) * (f_mq136(20, 65) / f_mq136(T, H))**(-3.74531835206)

# Testing the formulas with sample data
if __name__ == "__main__":
    currentHumidity = 32
    currentTemperature = 67
    
    # MQ9 calculations => lp value is around 0.4
    currentPpm = 0.4
    meanRs = 670
    # MQ9 calculations
    experimentVal_mq9 = getRatio_mq9(currentPpm) * f_mq9(currentTemperature, currentHumidity) / f_mq9(20, 65)
    calculatedRo_mq9 = meanRs / experimentVal_mq9
    print("Calculated Ro_mq9: ", calculatedRo_mq9)
    print(formula_mq9(currentHumidity, currentTemperature, meanRs, calculatedRo_mq9))

    # MQ7 calculations
    currentPpm_mq7 = 6 # co value is around 0.4
    meanRs = 2600
    experimentVal_mq7 = getRatio_mq7(currentPpm_mq7) * f_mq7(currentTemperature, currentHumidity) / f_mq7(20, 65)
    calculatedRo_mq7 = meanRs / experimentVal_mq7
    print("Calculated Ro_mq7: ", calculatedRo_mq7)
    print(formula_mq7(currentHumidity, currentTemperature, meanRs, calculatedRo_mq7))

    # MQ136 calculations --> h2s value is around 0.3
    currentPpm_mq136 = 0.3
    meanRs = 2700
    experimentVal_mq136 = getRatio_mq136(currentPpm_mq136) * f_mq136(currentTemperature, currentHumidity) / f_mq136(20, 65)
    calculatedRo_mq136 = meanRs / experimentVal_mq136
    print("Calculated Ro_mq136: ", calculatedRo_mq136)
    print(formula_mq136(currentHumidity, currentTemperature, meanRs, calculatedRo_mq136))

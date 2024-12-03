#include <Arduino.h>
#include <math.h>


int sensorPin_0564 = 15;
int Ro_0564 = 1;
#define Vc 3.3
class SEN0564_GasSensor {
public:
    // Coefficients for Rs/Ro calculation
    const float a = 1.7901285236777154;
    const float b1 = -0.020923638050983233;
    const float b2 = -1.6076406512106393e-05;
    const float b3 = -0.012004842116623383;
    const float b4 = 1.3977402911589597e-05;
    const float b5 = 8.30860122e-05;

    // Lookup table data (ppm, Rs/Ro)
    float points[9][2] = {
        {1.045800744138103, 0.7584065017590683},
        {5.01374306822658, 0.5383427435831706},
        {9.962750503745998, 0.40405634660838996},
        {19.796865585096565, 0.2869508626557279},
        {49.95067127862733, 0.21319016796829118},
        {99.25639759989119, 0.16826132407456496},
        {146.32416193145502, 0.14250821259459714},
        {497.64607544359575, 0.11764684461249969},
        {1003.7388767529611, 0.112965730111953}
    };
    float points1[9][2] = {
        {1003.7388767529611, 0.112965730111953},
        {497.64607544359575, 0.11764684461249969},
        {146.32416193145502, 0.14250821259459714},
        {99.25639759989119, 0.16826132407456496},
        {49.95067127862733, 0.21319016796829118},
        {19.796865585096565, 0.2869508626557279},
        {9.962750503745998, 0.40405634660838996},
        {5.01374306822658, 0.5383427435831706},
        {1.045800744138103, 0.7584065017590683}
    };

    // Function to calculate Rs/Ro based on temperature (T) and humidity (H)
    float calculateRsRo(float T, float H) {
        float rs_ro = a + b1 * T + b2 * T * T + b3 * H + b4 * H * H + b5 * T * H;
        return rs_ro;
    }

    // Function to interpolate ppm based on Rs/Ro value
    float interpolateLogRsRo(float rs_ro_value) {
        // Check if Rs/Ro is outside the bounds
        if (rs_ro_value < points1[0][1] || rs_ro_value > points1[8][1]) {
            Serial.println("Rs/Ro value is out of bounds.");
            return NAN; // Return NaN for out of bounds
        }

        // Find the two closest Rs/Ro points (R1, R2)
        for (int i = 0; i < 8; i++) {
            if (points1[i][1] <= rs_ro_value && points1[i + 1][1] >= rs_ro_value) {
                // Perform logarithmic interpolation
                float log_r1 = log(points1[i][1]);
                float log_r2 = log(points1[i + 1][1]);
                float log_ppm1 = log(points1[i][0]);
                float log_ppm2 = log(points1[i + 1][0]);
                float log_ppm_value = log_ppm1 + (log_ppm2 - log_ppm1) * (log(rs_ro_value) - log_r1) / (log_r2 - log_r1);
                return exp(log_ppm_value); // Return the result in original space 
            }
        }

        return NAN; // Return NaN if not found (should not happen)
    }

    // Function to calculate concentration based on Rs/Ro value, T, and H
    float calculateConcentration(float rs_ro_value, float T, float H) {
        float concentration = interpolateLogRsRo(rs_ro_value);
        return concentration * calculateRsRo(20, 55) / calculateRsRo(T, H);
    }

    // Function to interpolate Rs/Ro for a given ppm value
    float interpolateLogPpm(float ppm_value) {
        // Check if ppm is outside the bounds
        if (ppm_value < points[0][0] || ppm_value > points[8][0]) {
            Serial.println("ppm value is out of bounds.");
            return NAN; // Return NaN for out of bounds
        }

        // Find the two closest ppm points (ppm1, ppm2)
        for (int i = 0; i < 8; i++) {
            if (points[i][0] <= ppm_value && points[i + 1][0] >= ppm_value) {
                // Perform logarithmic interpolation
                float log_ppm1 = log(points[i][0]);
                float log_ppm2 = log(points[i + 1][0]);
                float log_r1 = log(points[i][1]);
                float log_r2 = log(points[i + 1][1]);
                float log_rs_ro_value = log_r1 + (log_r2 - log_r1) * (log(ppm_value) - log_ppm1) / (log_ppm2 - log_ppm1);
                Serial.println("Caliberated");
                return exp(log_rs_ro_value); // Return the result in original space
            }
        }

        return NAN; // Return NaN if not found (should not happen)
    }

    // Function to calculate Ro based on Rs, T, H, and ppm
    float calculateRo(float rs_value, float T, float H, float ppm) {
        float rs_ro = interpolateLogPpm(ppm) * calculateRsRo(T, H) / calculateRsRo(20, 55);
        return rs_value / rs_ro;
    }
};

// Example usage
SEN0564_GasSensor sen0564Sensor;

void setup() {
    Serial.begin(115200);
    delay(1000);

     // Read the analog value from the sensor pin
    int sensorValue_0564 = analogRead(sensorPin_0564); 

    // Convert the analog reading to voltage (VRL_0564)
    float VRL_0564 = sensorValue_0564 * (Vc / 4095.0); // Assuming Vc is your reference voltage (5V or 3.3V)

    // Calculate Rs_0564 (sensor resistance) based on VRL_0564
    float Rs_0564 = ((Vc - VRL_0564) / VRL_0564) * 4700; // Adjust 500 based on your sensor's load resistor value

    // Calculate Rs/Ro ratio
    // float RsRo_0564 = Rs_0564 / Ro_0564; // Ro_0564 should be a calibrated value
    Serial.print("Setup begins!");
    // Output values to the Serial Monitor
    Serial.print("Analog value: ");
    Serial.print(sensorValue_0564);
    Serial.print("  |  VRL_0564: ");
    Serial.print(VRL_0564);
    Serial.print(" V  |  Rs_0564: ");
    Serial.print(Rs_0564);
    Serial.print(" Ohms  |  Ro: ");
    // Serial.println(RsRo_0564);

    float given_Rs = Rs_0564;
    float T = 28;
    float H = 70;
    float given_ppm = 6;

    float ro_value = sen0564Sensor.calculateRo(given_Rs, T, H, given_ppm);
    Serial.println(ro_value); // Output the calculated Ro value
    Serial.print("Caliberated at ppm:");
    Serial.println(given_ppm);
    Ro_0564 = ro_value;
    Serial.print("Setup ends!");
}

void loop() {
    // Read the analog value from the sensor pin
    int sensorValue_0564 = analogRead(sensorPin_0564); 

    // Convert the analog reading to voltage (VRL_0564)
    float VRL_0564 = sensorValue_0564 * (Vc / 4095.0); // Assuming Vc is your reference voltage (5V or 3.3V)

    // Calculate Rs_0564 (sensor resistance) based on VRL_0564
    float Rs_0564 = ((Vc - VRL_0564) / VRL_0564) * 4700; // Adjust 500 based on your sensor's load resistor value

    // Calculate Rs/Ro ratio
    float RsRo_0564 = Rs_0564 / Ro_0564; // Ro_0564 should be a calibrated value

    // Output values to the Serial Monitor
    Serial.print("Analog value: ");
    Serial.print(sensorValue_0564);
    Serial.print("  |  VRL_0564: ");
    Serial.print(VRL_0564);
    Serial.print(" V  |  Rs_0564: ");
    Serial.print(Rs_0564);
    Serial.print(" Ohms  |  Rs/Ro: ");
    Serial.print(RsRo_0564);
    Serial.print(" | Ro: ");
    Serial.println(Ro_0564);
    float T = 28;
    float H =70;
    Serial.print("Ppm: ");
    Serial.println(sen0564Sensor.calculateConcentration(RsRo_0564, T,H));

    delay(1000); // Delay for readability
}
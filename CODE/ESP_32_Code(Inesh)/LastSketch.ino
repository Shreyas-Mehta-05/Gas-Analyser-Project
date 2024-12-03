#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <LiquidCrystal.h>
#include "pitches.h"
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
// Initialize GPS library
TinyGPSPlus gps;
// Wi-Fi credentials
const char* ssid = "POCO X3 Pro";
const char* password = "Lessgo69";

// Initialize hardware serial (Serial2) for Neo-6M
HardwareSerial gpsSerial(2); // Using Serial 2 on ESP32 (TX: GPIO 17, RX: GPIO 16)

// Define OLED display dimensions
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// OLED reset pin (-1 if not connected)
#define OLED_RESET    -1

// OLED I2C address (0x3C for most SSD1306 displays)
#define SCREEN_ADDRESS 0x3C

// Create SSD1306 display object
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Pin assignments for I2C
const int SDA_PIN = 21;
const int SCL_PIN = 22;

// Variable to track if GPS is connected
bool gpsConnected = false;




// MQTT Credentials for MQ-7 sensor
#define MQ7_MQTT_USERNAME "FTcqMTAMHActGjciEQIHHQ0"
#define MQ7_MQTT_CLIENT_ID "FTcqMTAMHActGjciEQIHHQ0"
#define MQ7_MQTT_PASSWORD "AFRuARv2GltBhfk8VTL/AUDb"

// MQTT Credentials for DHT11 sensor
#define DHT_MQTT_USERNAME "AS41AxwNJSokITwQPS0HIyM"
#define DHT_MQTT_CLIENT_ID "AS41AxwNJSokITwQPS0HIyM"
#define DHT_MQTT_PASSWORD "M6htydKJkeityX0hRo9KPMaQ"

// MQTT Credentials for MQ-9 sensor
#define MQ9_MQTT_USERNAME "FjY0Nx88HisdIg42KDw2Ayk"
#define MQ9_MQTT_CLIENT_ID "FjY0Nx88HisdIg42KDw2Ayk"
#define MQ9_MQTT_PASSWORD "hfOGB7fZXHGJ/3TueSHJHUjW"

// MQTT Credentials for MQ-136 sensor
#define MQ136_MQTT_USERNAME "BSU5NCgcFR00DSAANwcFHxA"
#define MQ136_MQTT_CLIENT_ID "BSU5NCgcFR00DSAANwcFHxA"
#define MQ136_MQTT_PASSWORD "eJDpmpntFIWZrkdcl+DWJjjI"

// ThingSpeak channel ID and topic
const char* channelID = "2677015";
String topic = "channels/" + String(channelID) + "/publish";

// MQTT Server
const char* mqttServer = "mqtt3.thingspeak.com";
const int mqttPort = 1883;

// Pin definitions
int mq7Pin = 34;      // D5 for MQ-7 sensor
int mq9Pin = 32;      // D6 for MQ-9 sensor
int mq136Pin = 33;    // D7 for MQ-136 sensor
#define DHTPIN 2
#define DHTTYPE DHT11
#define BUZZER_PIN 15

int currentDisplay = 0; // To track the current display being shown
unsigned long lastDisplayUpdate = 0;  // Initialize last display update time
const unsigned long displayInterval = 3000; // Rotate every 3 seconds

// DHT11 sensor initialization
DHT dht(DHTPIN, DHTTYPE);

// Initialize Wi-Fi and MQTT clients
WiFiClient espClientMQ7;
PubSubClient clientMQ7(espClientMQ7);

WiFiClient espClientDHT;
PubSubClient clientDHT(espClientDHT);

WiFiClient espClientMQ9;
PubSubClient clientMQ9(espClientMQ9);

WiFiClient espClientMQ136;
PubSubClient clientMQ136(espClientMQ136);

// Constants for MQ-7 sensor
const float Vc = 3.3;    // Supply voltage, using 3.3V
const float RL = 1000;   // Load resistance in ohms (1kΩ) // mq 9 ka 500 ohms hai RL
const float Ro_MQ7 = 771.08; // Predefined Ro value for MQ-7
const float Ro_MQ9 = 18.154; // Predefined Ro value for MQ-9
const float Ro_MQ136 = 14634; // Predefined Ro value for MQ-136

// LCD Setup (adjust pins based on your setup)
// LiquidCrystal lcd(22, 21, 5, 18, 23, 19); // LCD connected to pins 22, 21, etc.

// Function to calculate f(T, H)
float f(float T, float H) {
  float a = 1.2094342542500245;
  float b1 = -0.01094546624860255;
  float b2 = 8.559231727624334e-05;
  float b3 = -2.220918787838429e-07;
  float b4 = -2.6206841578149175e-05;
  float b5 = 1.4963577356169694e-05;
  return (a + b1 * T + b2 * T * T + b3 * H + b4 * H * H + b5 * T * H);
}


float formula_MQ7(float H, float T, float Rs, float Ro = Ro_MQ7) {
  return (101.24201 * pow((Rs / Ro), -1.4792899)) * pow((f(20, 65) / f(T, H)), -1.4792899);
}

// Formula to calculate ppm for MQ-9 (LPG)
float formula_MQ9(float H, float T, float Rs, float Ro = Ro_MQ9) {
  return (963.40351 * pow((Rs / Ro), -2.16919739696)) * pow((f(20, 65) / f(T, H)), -2.16919739696);
}

// Formula to calculate ppm for MQ-136 (H2S)
float formula_MQ136(float H, float T, float Rs, float Ro = Ro_MQ136) {
  return (0.1342531 * pow((Rs / Ro), -3.74531835206)) * pow((f(20, 65) / f(T, H)), -3.74531835206);
}

// Function to connect to Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected with IP address: ");
  Serial.println(WiFi.localIP());
}

// Function to reconnect to MQTT for MQ-7
void reconnectMQ7() {
  while (!clientMQ7.connected()) {
    Serial.print("Attempting MQ-7 MQTT connection...");
    if (clientMQ7.connect(MQ7_MQTT_CLIENT_ID, MQ7_MQTT_USERNAME, MQ7_MQTT_PASSWORD)) {
      Serial.println("MQ-7 Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect MQ-7, rc=");
      Serial.print(clientMQ7.state());
      Serial.println(" trying again in 5 seconds...");
      delay(5000);
    }
  }
}

// Function to reconnect to MQTT for DHT11
void reconnectDHT() {
  while (!clientDHT.connected()) {
    Serial.print("Attempting DHT11 MQTT connection...");
    if (clientDHT.connect(DHT_MQTT_CLIENT_ID, DHT_MQTT_USERNAME, DHT_MQTT_PASSWORD)) {
      Serial.println("DHT11 Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect DHT11, rc=");
      Serial.print(clientDHT.state());
      Serial.println(" trying again in 5 seconds...");
      delay(5000);
    }
  }
}

// Function to reconnect to MQTT for MQ-9
void reconnectMQ9() {
  while (!clientMQ9.connected()) {
    Serial.print("Attempting MQ-9 MQTT connection...");
    if (clientMQ9.connect(MQ9_MQTT_CLIENT_ID, MQ9_MQTT_USERNAME, MQ9_MQTT_PASSWORD)) {
      Serial.println("MQ-9 Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect MQ-9, rc=");
      Serial.print(clientMQ9.state());
      Serial.println(" trying again in 5 seconds...");
      delay(5000);
    }
  }
}

// Function to reconnect to MQTT for MQ-136
void reconnectMQ136() {
  while (!clientMQ136.connected()) {
    Serial.print("Attempting MQ-136 MQTT connection...");
    if (clientMQ136.connect(MQ136_MQTT_CLIENT_ID, MQ136_MQTT_USERNAME, MQ136_MQTT_PASSWORD)) {
      Serial.println("MQ-136 Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect MQ-136, rc=");
      Serial.print(clientMQ136.state());
      Serial.println(" trying again in 5 seconds...");
      delay(5000);
    }
  }
}

// void updateDisplay(float temp, float humidity, float ppm_MQ7, float Rs_MQ7, 
//                    float ppm_MQ9, float Rs_MQ9, float ppm_MQ136, float Rs_MQ136,
//                    double latitude, double longitude) {
//   display.clearDisplay();
//   display.setTextSize(1);
//   display.setTextColor(SSD1306_WHITE);

//   switch (currentDisplay) {
//     case 0: // Display MQ-7 Sensor Data
//       display.setCursor(0, 0);
//       display.print("MQ-7 (CO)");
//       display.setCursor(0, 10);
//       display.print("Rs: ");
//       display.print(Rs_MQ7);
//       display.setCursor(0, 20);
//       display.print("PPM: ");
//       display.print(ppm_MQ7);
//       break;

//     case 1: // Display MQ-9 Sensor Data
//       display.setCursor(0, 0);
//       display.print("MQ-9 (LPG)");
//       display.setCursor(0, 10);
//       display.print("Rs: ");
//       display.print(Rs_MQ9);
//       display.setCursor(0, 20);
//       display.print("PPM: ");
//       display.print(ppm_MQ9);
//       break;

//     case 2: // Display MQ-136 Sensor Data
//       display.setCursor(0, 0);
//       display.print("MQ-136 (H2S)");
//       display.setCursor(0, 10);
//       display.print("Rs: ");
//       display.print(Rs_MQ136);
//       display.setCursor(0, 20);
//       display.print("PPM: ");
//       display.print(ppm_MQ136);
//       break;

//     case 3: // Display Temperature and Humidity
//       display.setCursor(0, 0);
//       display.print("DHT11 Sensor");
//       display.setCursor(0, 10);
//       display.print("Temp: ");
//       display.print(temp);
//       display.print("C");
//       display.setCursor(0, 20);
//       display.print("Hum: ");
//       display.print(humidity);
//       display.print("%");
//       break;

//     case 4: // Display GPS Data
//       display.setCursor(0, 0);
//       display.print("GPS Data");
//       display.setCursor(0, 10);
//       display.print("Lat: ");
//       display.print(latitude, 6);
//       display.setCursor(0, 20);
//       display.print("Lng: ");
//       display.print(longitude, 6);
//       break;
//   }

//   display.display();
//   currentDisplay = (currentDisplay + 1) % 5; // Cycle through 5 screens
// }
void updateDisplay(float temp, float humidity, float ppm_MQ7, float Rs_MQ7, 
                   float ppm_MQ9, float Rs_MQ9, float ppm_MQ136, float Rs_MQ136,
                   double latitude, double longitude) {
  // Clear display and set text size and color
  display.clearDisplay();
  display.setTextSize(1); // Small text for data values
  display.setTextColor(SSD1306_WHITE);
  
  // Calculate the center for the screen
  int centerX = 64;  // Middle of the 128-pixel wide display
  int centerY = 32;  // Middle of the 64-pixel high display
  int textHeight = 24; // Height of 3 lines of text at textSize(1)
  int offsetY = centerY - textHeight / 2; // Center vertically

  // Full-screen border
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE); // Full screen border

  // Middle border (slightly smaller)
  display.drawRect(5, 5, 118, 54, SSD1306_WHITE); // Middle border, offset by 5 pixels

  // Bottom border (even smaller)
  display.drawRect(10, 10, 108, 44, SSD1306_WHITE); // Bottom section border

  // Switch between different display modes
  switch (currentDisplay) {
    case 0: // Display MQ-7 Sensor Data (CO)
      display.setCursor(centerX - (strlen("MQ-7 (CO)") * 6) / 2, offsetY);  // Center the title
      display.print("MQ-7 (CO)");

      display.setCursor(centerX - (strlen("Rs: ") * 6) / 2 - 15, offsetY + 10); // Larger offset for "Rs:"
      display.print("Rs: ");
      display.print(Rs_MQ7, 2);  // Show Rs with 2 decimal places

      display.setCursor(centerX - (strlen("PPM: ") * 6) / 2 - 10, offsetY + 20); // Larger offset for "PPM:"
      display.print("PPM: ");
      display.print(ppm_MQ7, 2); // Show PPM with 2 decimal places
      break;

    case 1: // Display MQ-9 Sensor Data (LPG)
      display.setCursor(centerX - (strlen("MQ-9 (LPG)") * 6) / 2, offsetY);  // Center the title
      display.print("MQ-9 (LPG)");

      display.setCursor(centerX - (strlen("Rs: ") * 6) / 2 - 15, offsetY + 10); // Larger offset for "Rs:"
      display.print("Rs: ");
      display.print(Rs_MQ9, 2);

      display.setCursor(centerX - (strlen("PPM: ") * 6) / 2 - 10, offsetY + 20); // Larger offset for "PPM:"
      display.print("PPM: ");
      display.print(ppm_MQ9, 2);
      break;

    case 2: // Display MQ-136 Sensor Data (H2S)
      display.setCursor(centerX - (strlen("MQ-136 (H2S)") * 6) / 2 +5, offsetY);  // Center the title
      display.print("MQ-136 (H2S)");

      display.setCursor(centerX - (strlen("Rs: ") * 6) / 2 - 15, offsetY + 10); // Larger offset for "Rs:"
      display.print("Rs: ");
      display.print(Rs_MQ136, 2);

      display.setCursor(centerX - (strlen("PPM: ") * 6) / 2 - 10, offsetY + 20); // Larger offset for "PPM:"
      display.print("PPM: ");
      display.print(ppm_MQ136, 2);
      break;

    case 3: // Display Temperature and Humidity from DHT11
      display.setCursor(centerX - (strlen("DHT11 Sensor") * 6) / 2 + 5 , offsetY);  // Center the title
      display.print("DHT11 Sensor");

      display.setCursor(centerX - (strlen("Temp: ") * 6) / 2 - 10, offsetY + 10); // Larger offset for "Temp:"
      display.print("Temp: ");
      display.print(temp, 1);  // Show Temp with 1 decimal place
      display.print("C");

      display.setCursor(centerX - (strlen("Hum: ") * 6) / 2 - 10, offsetY + 20); // Larger offset for "Hum:"
      display.print("Hum: ");
      display.print(humidity, 1);  // Show Humidity with 1 decimal place
      display.print("%");
      break;

    case 4: // Display GPS Data (Latitude and Longitude)
      display.setCursor(centerX - (strlen("GPS Data") * 6) / 2, offsetY);  // Center the title
      display.print("GPS Data");

      display.setCursor(centerX - (strlen("Lat: ") * 6) / 2 - 25, offsetY + 10); // Larger offset for "Lat:"
      display.print("Lat: ");
      display.print(latitude, 6); // Show Latitude with 6 decimal places

      display.setCursor(centerX - (strlen("Lng: ") * 6) / 2 - 25, offsetY + 20); // Larger offset for "Lng:"
      display.print("Lng: ");
      display.print(longitude, 6); // Show Longitude with 6 decimal places
      break;
  }

  // Draw a separator line between the sections
  // display.drawLine(0, 32, 128, 32, SSD1306_WHITE); // Horizontal separator line at the center of the display

  // Update the display
  display.display();

  // Cycle through 5 screens
  currentDisplay = (currentDisplay + 1) % 5;
}





void setup() {
  // Start Serial Monitor
  Serial.begin(115200);

  // Connect to Wi-Fi
  setup_wifi();

  // Set MQTT servers for all clients
  clientMQ7.setServer(mqttServer, mqttPort);
  clientDHT.setServer(mqttServer, mqttPort);
  clientMQ9.setServer(mqttServer, mqttPort);
  clientMQ136.setServer(mqttServer, mqttPort);

  // Connect to MQTT brokers
  reconnectMQ7();
  reconnectDHT();
  reconnectMQ9();
  reconnectMQ136();

  // Initialize DHT11 sensor and LCD
  Serial.println("Initializing DHT11 sensor...");
  dht.begin();

  // Start GPS communication with the correct baud rate (9600) on Serial2
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);
  Serial.println("GPS module initialized. Waiting for data...");

  // lcd.begin(16, 2);   // LCD setup with 16 columns and 2 rows
  // lcd.clear();
  pinMode(BUZZER_PIN, OUTPUT);  // Initialize Buzzer

  // Start I2C communication on specified SDA and SCL pins
  Wire.begin(SDA_PIN, SCL_PIN);
  Serial.println("I2C communication started with SDA on pin 21 and SCL on pin 22.");

  // Try to initialize the display
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 OLED not detected - Not working."));
    while (true); // Stop program if initialization fails
  }

  // If the display is initialized successfully
  Serial.println("SSD1306 OLED detected - Working.");
  
  // Clear the display buffer and show "Working" on the OLED screen
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Starting");
  display.display();  // Show "Working" on the OLED
  
  // Print to the Serial Monitor as well
  Serial.println("OLED is working and displaying 'Working'.");

}

void loop() {
  // Ensure all MQTT clients are connected
  if (!clientMQ7.connected()) {
    reconnectMQ7();
  }
  if (!clientDHT.connected()) {
    reconnectDHT();
  }
  if (!clientMQ9.connected()) {
    reconnectMQ9();
  }
  if (!clientMQ136.connected()) {
    reconnectMQ136();
  }

  clientMQ7.loop();
  clientDHT.loop();
  clientMQ9.loop();
  clientMQ136.loop();

  // --- MQ-7 Sensor Data ---
  int analogValue_MQ7 = analogRead(mq7Pin);  // Analog reading from MQ-7
  float VRL = analogValue_MQ7 * (Vc / 4095.0);  // Convert analog value to voltage
  float Rs_MQ7 = ((Vc - VRL) / VRL) * RL;       // Calculate Rs
  float RsRo_MQ7 = Rs_MQ7 / Ro_MQ7;             // Calculate Rs/Ro

  float ppm_MQ7 = formula_MQ7(65, 20, Rs_MQ7, Ro_MQ7);
  Serial.print("MQ-7 Rs: ");
  Serial.print(Rs_MQ7);
  Serial.print(" Ohms, CO PPM: ");
  Serial.println(ppm_MQ7);

  // Publish data to ThingSpeak
  String payloadMQ7 = "field1=" + String(RsRo_MQ7) + "&field2=" + String(ppm_MQ7);
  clientMQ7.publish(topic.c_str(), payloadMQ7.c_str());
  delay(2000);

  // --- DHT11 Sensor Data ---
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (!isnan(humidity) || !isnan(temperature)) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

    // Publish data to ThingSpeak
    String payloadDHT = "field7=" + String(temperature) + "&field8=" + String(humidity);
    clientDHT.publish(topic.c_str(), payloadDHT.c_str());
    delay(2000);
  }
  else {
    // If readings are invalid, print an error message
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
}

  // --- MQ-9 Sensor Data ---
  int analogValue_MQ9 = analogRead(mq9Pin);
  float VRL_MQ9 = analogValue_MQ9 * (Vc / 4095.0); 
  float Rs_MQ9 = ((Vc - VRL_MQ9) / VRL_MQ9) * 500;
  float RsRo_MQ9 = Rs_MQ9 / Ro_MQ9;             // Calculate Rs/Ro

  float ppm_MQ9 = formula_MQ9(65, 20, Rs_MQ9, Ro_MQ9);
  Serial.print("MQ-9 Rs: ");
  Serial.print(Rs_MQ9);
  Serial.print(" Ohms, LPG PPM: ");
  Serial.println(ppm_MQ9);

  // Publish data to ThingSpeak
  String payloadMQ9 = "field3=" + String(Rs_MQ9) + "&field4=" + String(ppm_MQ9);
  clientMQ9.publish(topic.c_str(), payloadMQ9.c_str());
  delay(2000);

  // --- MQ-136 Sensor Data ---
  int analogValue_MQ136 = analogRead(mq136Pin);
  float VRL_MQ136 = analogValue_MQ136 * (Vc / 4095.0); 
  float Rs_MQ136 = ((Vc - VRL_MQ136) / VRL_MQ136) * RL;
  float RsRo_MQ136 = Rs_MQ136 / Ro_MQ136;       // Calculate Rs/Ro

  float ppm_MQ136 = formula_MQ136(65, 20, Rs_MQ136, Ro_MQ136);
  Serial.print("MQ-136 Rs: ");
  Serial.print(Rs_MQ136);
  Serial.print(" Ohms, H2S PPM: ");
  Serial.println(ppm_MQ136);

  // Publish data to ThingSpeak
  String payloadMQ136 = "field5=" + String(Rs_MQ136) + "&field6=" + String(ppm_MQ136);
  clientMQ136.publish(topic.c_str(), payloadMQ136.c_str());
  delay(2000);


  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    gpsConnected = true; // Set to true if any data is received
  }
  // If GPS has received data, display location info
  float latitude = 0 ;
  float longitude = 0;
  if (gpsConnected) {
    if (gps.location.isUpdated()) {
      Serial.print("Latitude: ");
      latitude = gps.location.lat();
      Serial.println(latitude,6); // 6 decimal places
      Serial.print("Longitude: ");
      longitude = gps.location.lng();
      Serial.println(longitude,6);
      Serial.print("Altitude: ");
      Serial.println(gps.altitude.meters());
      Serial.print("Satellites: ");
      Serial.println(gps.satellites.value());
      Serial.print("Speed: ");
      Serial.println(gps.speed.kmph());
    } else {
      // If GPS is connected but no valid data yet, display a message
      Serial.println("GPS connected but no valid location data yet.");
    }
  } else {
    // If no data is received, display a connection error
    Serial.println("GPS module not connected or no data received.");
  }

  // Reset connection status for the next loop
  gpsConnected = false;
  delay(2000);
  if (millis() - lastDisplayUpdate >= displayInterval) {
    updateDisplay(temperature, humidity, ppm_MQ7, Rs_MQ7, ppm_MQ9, Rs_MQ9, ppm_MQ136, Rs_MQ136, latitude, longitude);
    lastDisplayUpdate = millis();
  }
}
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

const char* ssid = "***";
const char* password = "***";
String serverName = "IP:5000/data";

Adafruit_AHTX0 aht;
Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Verbinding met WiFi...");
  }
  Serial.println("Verbonden met WiFi");

  if (!aht.begin()) {
    Serial.println("AHT20 niet gevonden");
  }
  if (!bmp.begin()) {
    Serial.println("BMP280 niet gevonden");
  }
}

void loop() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  float pressure = bmp.readPressure() / 100.0;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String data = "{\"temperature\":";
    data += temp.temperature;
    data += ",\"humidity\":";
    data += humidity.relative_humidity;
    data += ",\"pressure\":";
    data += pressure;
    data += "}";

    http.POST(data);
    http.end();
  }

  delay(60 * 1000); 
}

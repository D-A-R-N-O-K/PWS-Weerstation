#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

Adafruit_BMP280 bmp;
Adafruit_AHTX0 aht;

void setup() {
  Serial.begin(115200);
  
  if (!bmp.begin()) Serial.println("BMP280 nicht gefunden!");
  if (!aht.begin()) Serial.println("AHT nicht gefunden!");
}

void loop() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  float pressure = bmp.readPressure() / 100.0F; // hPa
  float temperature = temp.temperature;
  float hum = humidity.relative_humidity;

  // JSON-formatierte Daten über Serial senden
  Serial.print("{\"temperature\":");
  Serial.print(temperature);
  Serial.print(",\"humidity\":");
  Serial.print(hum);
  Serial.print(",\"pressure\":");
  Serial.print(pressure);
  Serial.println("}");

  delay(60 * 1000); // alle 5 Minuten
}

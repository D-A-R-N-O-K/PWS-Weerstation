// Inclusie van benodigde bibliotheken
#include <Arduino.h>          // Standaard Arduino bibliotheek
#include <Wire.h>             // Voor I2C communicatie met sensoren
#include <Adafruit_BMP280.h>  // Bibliotheek voor BMP280 luchtdruk- en temperatuursensor
#include <Adafruit_AHTX0.h>   // Bibliotheek voor AHT20 temperatuur- en luchtvochtigheidssensor

// Initialiseer sensor objecten
Adafruit_BMP280 bmp;  // Object voor BMP280 sensor
Adafruit_AHTX0 aht;   // Object voor AHT20 sensor

void setup() {
  // Start seriële communicatie met 115200 baud
  Serial.begin(115200);
  
  // Initialiseer sensoren en controleer of ze gevonden zijn
  if (!bmp.begin()) Serial.println("BMP280 niet gevonden!");
  if (!aht.begin()) Serial.println("AHT niet gevonden!");
}

void loop() {
  // Variabelen voor sensorgegevens
  sensors_event_t humidity, temp;
  
  // Lees temperatuur en luchtvochtigheid van AHT20 sensor
  aht.getEvent(&humidity, &temp);

  // Lees luchtdruk van BMP280 sensor en converteer naar hPa
  float pressure = bmp.readPressure() / 100.0F; // hPa
  float temperature = temp.temperature;          // Temperatuur in °C
  float hum = humidity.relative_humidity;       // Luchtvochtigheid in %

  // Verzend sensorgegevens als JSON via seriële poort
  Serial.print("{\"temperature\":");
  Serial.print(temperature);
  Serial.print(",\"humidity\":");
  Serial.print(hum);
  Serial.print(",\"pressure\":");
  Serial.print(pressure);
  Serial.println("}");

  // Wacht 1 minuut voor de volgende meting (60 seconden * 1000 milliseconden)
  delay(60 * 1000);
}

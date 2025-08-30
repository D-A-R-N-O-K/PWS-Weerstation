# Concept
Hoe moeielijk is het om een eigen weerstation te maken?  
Hoe betrowbaar kunnen wij voorspellingen met deze weerstation maken?
## Functies/Data:
- Neerslag
- Onweer/Bliksem (waarschuwing)
- Temperatuur
- Luchtvochtigheid
- Luchtdrukte 
- UV-Index
- Zonsopgang en zonsondergang (Ook maan...)
- Windrichting
- Windsterkte (beaufort/km/h)
- Autonoom (via dynamo (wind) of solar?)
- Weergave (Website en Bluetooth/WiFi? (Stationair voor thuis?))
- Dew Point?
- AQI?
- Visibility?
- Wolken?
- Weervoorspellingen

## Code
Het belangrijkste onderdeel van dit project is de code.  
### Taal  
De code gaan we waarschijnlijk schrijven in Python, de populairste code taal ter wereld.
We hebben Python gekozen omdat het eenvoudiger is dan C++ en niet gecompileerd moet worden, dus is het handiger bij veel trial & error.
Nativ werkt de ESP32 die we gaan gebruiken voor dit project, met C++.
Om nu in Python te kunnen progameren moeten wij de ESP32 met micropython flashen.  

### Structuur  
1. Sensor-block
   - sensor data wordt gelezen
2. Verwerking-block
   - data wordt geconverteerd naar eenheden
   - gemiddelde\mediaan wordt berekend
   - corrupte data wordt gefilterd
   - analyseert data (voorspellingen)
3. Communicatie-block
   - data wordt doorgestuurd aan bijv.:
     - server
     - andere ESP32
     - beeldscherm
     - geheugen (USB etc.)
     - terminal
     - website (van de ESP32 gehostet)
4. Client side (Tweede ESP32)
   - ontvangt data van weerstation
   - analyseert data (voorspellingen)
   - geeft data weer

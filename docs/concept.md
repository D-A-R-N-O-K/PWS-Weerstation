# Concept
Hoe moeielijk is het om een eigen weerstation te maken?  
Hoe betrowbaar kunnen wij voorspellingen met deze weerstation maken?
## Functies/Data:
- Neerslag
- Onweer/Bliksem (waarschuwing) x
- Temperatuur
- Luchtvochtigheid
- Luchtdrukte 
- UV-Index x
- Zonsopgang en zonsondergang (Ook maan...) x
- Windrichting x
- Windsterkte (beaufort/km/h)
- Autonoom (via dynamo (wind) of solar?) x
- Weergave (Website en Bluetooth/WiFi? (Stationair voor thuis?)) 
- Dew Point?
- AQI?
- Visibility? x
- Wolken? x
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
3. Communicatie-block
   - data wordt doorgestuurd aan bijv.:
     - server
     - andere ESP32
     - beeldscherm
     - geheugen (USB etc.)
     - terminal
     - website (van de ESP32 gehostet)
     - raspberry pi server (voor analyse)
4. Client side (Tweede ESP32)
   - ontvangt data van weerstation
   - geeft data weer

### Libraries (c++ in IDE)  
- Arduino esp32 Boards by Espressif 
- DHT sensor library by Adafruit  
- 

## Analyse
Met de gemeten data gaan we proberen om weervoorspellingen de maken.  
We gaan dit proberen met een Raspberry Pi, die we voeden met de verzamelde data, zodat hij door middel van ML (machine learning) patronen in de data begint te herkennen en zo voorspellingen kan genereren. 

Voorbeeld:  
de luchtdruk daalt, het weer verslechtert (meer bewolking, regen enz.). De volgende keer dat de Raspberry Pi in de data herkent dat de luchtdruk daalt, voorspelt hij dat het weer slechter wordt. 

Met behulp van ML hopen we dat deze voorspellingen steeds nauwkeuriger worden. Na verloop van tijd zullen we deze voorspellingen vergelijken met de voorspellingen van gerenommeerde websites en de verschillen analyseren.


Naar meer onderzoek hebben we besloten om de de open-source python library "River" te gebruiken voor het ML. We hebben voor River gekozen omdat het heel makkelijk is om ins project te gebruiken omdat we sowieso vooral python willen gebruiken.

We moeten wel nog overleggen hoe we makkelijk kunnen documenteren of de voorspellingen wel of niet kloppen. Deze data gaan we dan proberen met een [graph te visualieseren](grafana.org) en dan met data van bekende "Weerapps" te verglijken.

## Literatuuronderzoek
Onderzoek naar meetapparatuur/binaire waarden.

## Onderzoek
Het doel van deze PWS is om de volgende vragen te kunnen beantwoorden:

1. **In hoeverre is het mogelijk om een eigenweerstation te maken?**
2. Hoe nauwkeurig kunnen we zelfs voorspellingen maken?
3. Hoe vaak (%) kloppen oze voorspellingen in vergelijking met andere websites/apps?
4. ...

## ontwerpeisen
Voordat we het gehele ontwerp kunnen gaan maken moeten eerst de ontwerpeisen duidelijk zijn. Dit voorkomt problemen in latere delen van ons project zoals overcomplicatie of juist een te gebrekkig ontwerp.  
Door te bepalen wat de functies moeten zijn, wordt dit geprobeert te vermijden.  
  
### Ontwerp risico's en maatregelen  
- Zelfwarming van sensoren (d.m.v. apparatuur of zonlicht)  
Oplossing: Afstand tussen warme elementen, genoeg ventilatie en koellichamen (heatsink)  
- Elektrische ruis, kan foutiefe metingen geven (externe bronnen of door de batterij)  
Oplossing: Afscherming van kabels (bij langere afstanden) en voor de voeding een decoupler capacitor (verder onderzoeken)  
- Condens, kan zorgen voor verkeerder meetingen (luchtvochtigheid  
Oplossing: Ademende waterdichte filters  
- Vibraties en lagerproblemen, kunnen windrichting/snelheid beinvloeden  
Oplossing: een stabiele ondergrond, goede lagers die ook gecalibreerd zijn (met dank aan Edgar Hek)  
- Timing van de componenten/ onderdelen voor gelijke tijden van metingen.  
Oplossing: Gebruik RTC of NTP.    
  
Minder belangrijke/rolspelende factoren:  
A/D converter moet een goede resolutie hebben. Het meetsignaal (analoog) moet in met de juiste nauwkeurigheid omgezet worden naar digitale waarden (bits).



## Plan van aanpak


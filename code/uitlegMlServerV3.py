# Import benodigde bibliotheken
import serial  # Voor seriële communicatie met Arduino
import json  # Voor het verwerken van JSON-data
from flask import Flask, render_template_string  # Voor het maken van een webserver
from river import linear_model, preprocessing  # Voor machine learning modellen
from datetime import datetime, timedelta  # Voor tijdsberekeningen
import math  # Voor wiskundige functies

app = Flask(__name__)  # Initialiseer Flask webapplicatie
data = []  # Lijst om meetgegevens op te slaan

# Maak een machine learning model voor temperatuurvoorspelling
# StandardScaler normaliseert de data, LinearRegression voorspelt de temperatuur
model = preprocessing.StandardScaler() | linear_model.LinearRegression()

# Serial-Port aanpassen (bijv. /dev/ttyACM0)
# 115200 baud rate, timeout van 1 seconde
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def read_from_esp():
    while True:
        try:
            # Lees een regel van de seriële poort en decodeer naar UTF-8
            # Negeer ongeldige bytes om fouten te voorkomen
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            # Verwerk alleen regels die eruitzien als JSON
            if line.startswith("{") and line.endswith("}"):
                try:
                    d = json.loads(line)  # Parse JSON-data
                    d["timestamp"] = datetime.now()  # Voeg tijdstempel toe
                    data.append(d)  # Sla data op in de lijst

                    # Bereid data voor voor het machine learning model
                    x = {"temp": d["temperature"], "humidity": d["humidity"], "pressure": d["pressure"]}
                    model.learn_one(x, d["temperature"])  # Train het model met de nieuwe data
                    print(f"[{datetime.now()}] Ontvangen: {d}")  # Log de ontvangen data
                except json.JSONDecodeError:
                    print(f"Ongeldige JSON: {line}")  # Foutmelding bij ongeldige JSON
        except Exception as e:
            print(f"Fout in Serial-Thread: {e}")  # Algemene foutafhandeling


import threading

# Start een achtergrondthread om continu data van de ESP32 te lezen
# daemon=True betekent dat de thread automatisch stopt wanneer het hoofdprogramma stopt
esp_thread = threading.Thread(target=read_from_esp, daemon=True)
esp_thread.start()

@app.route("/")
def index():
    # Webpagina route voor de hoofdpagina
    if not data:
        return "Nog geen data"  # Geen data beschikbaar

    # Haal de laatste meetgegevens op
    last = data[-1]
    predictions = []
    
    # Bereid inputdata voor voor het model
    x = {"temp": last["temperature"], "humidity": last["humidity"], "pressure": last["pressure"]}
    now = datetime.now()
    
    # Maak 48-uurs voorspelling (elk uur)
    for i in range(48):
        pred_temp = model.predict_one(x)  # Voorspel temperatuur
        predictions.append((now + timedelta(hours=i+1), pred_temp))  # Sla voorspelling op
        x["temp"] = pred_temp  # Gebruik voorspelde temperatuur voor volgende voorspelling

    # HTML sjabloon voor de webpagina
    html = """
   <!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<title>Weerstation Zwaag</title>

<style>
:root {
    --bg: #0f172a;
    --card: #111827;
    --text: #e5e7eb;
    --muted: #9ca3af;
    --accent: #38bdf8;
    --border: #1f2933;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 24px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
}

h1 { margin-bottom: 4px; }
h2 { margin-top: 0; }

.subtitle {
    color: var(--muted);
    margin-bottom: 24px;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
}

.metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
}

.metric {
    background: #020617;
    border-radius: 10px;
    padding: 12px;
}

.metric span {
    display: block;
    font-size: 0.85rem;
    color: var(--muted);
}

.metric strong {
    font-size: 1.4rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
}

th, td {
    padding: 10px 12px;
    text-align: left;
}

th {
    font-weight: 600;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
}

td {
    border-bottom: 1px solid var(--border);
}

tr:hover {
    background: rgba(56, 189, 248, 0.05);
}

.temp {
    color: var(--accent);
    font-weight: 600;
}
</style>
</head>

<body>

<h1>Weerstation Zwaag</h1>
<div class="subtitle">Stand: {{ now }}</div>

<div class="card">
  <h2>Actueele Meetingen</h2>
  <div class="metrics">
    <div class="metric">
      <span>Temperatuur</span>
      <strong>{{ temp }} °C</strong>
    </div>
    <div class="metric">
      <span>Luchtvochtigheid</span>
      <strong>{{ hum }} %</strong>
    </div>
    <div class="metric">
      <span>Luchtdruk</span>
      <strong>{{ pres }} hPa</strong>
    </div>
  </div>
</div>

<div class="card">
  <h2>Voorspelling (48uur)</h2>
  <table>
    <tr>
      <th>Tijd</th>
      <th>Temperatuur</th>
    </tr>
    {% for t, p in pred %}
    <tr>
      <td>{{ t }}</td>
      <td class="temp">{{ p|round(2) }} °C</td>
    </tr>
    {% endfor %}
  </table>
</div>

</body>
</html>
    """
    # Render de HTML pagina met de meetgegevens en voorspellingen
    return render_template_string(html,
                                  temp=last["temperature"],
                                  hum=last["humidity"],
                                  pres=last["pressure"],
                                  pred=predictions,
                                  now=now.strftime("%d-%m-%Y %H:%M"))

if __name__ == "__main__":
    # Start de Flask webserver
    # host="0.0.0.0" maakt de server toegankelijk op alle netwerkinterfaces
    # port=5000 is de standaard poort voor Flask
    app.run(host="0.0.0.0", port=5000)


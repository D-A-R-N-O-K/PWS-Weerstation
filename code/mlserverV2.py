from flask import Flask, request, render_template_string
from river import linear_model, preprocessing
from datetime import datetime, timedelta
import math

app = Flask(__name__)
data = []

model = preprocessing.StandardScaler() | linear_model.LinearRegression()

def time_features(ts: datetime):
    hour = ts.hour + ts.minute / 60
    day = ts.timetuple().tm_yday

    return {
        "hour_sin": math.sin(2 * math.pi * hour / 24),
        "hour_cos": math.cos(2 * math.pi * hour / 24),
        "day_sin": math.sin(2 * math.pi * day / 365),
        "day_cos": math.cos(2 * math.pi * day / 365),
    }

@app.route("/data", methods=["POST"])
def receive_data():
    incoming = request.get_json(force=True)
    if not incoming:
        return "No JSON received", 400

    try:
        temp = float(incoming.get("temperature"))
        hum  = float(incoming.get("humidity"))
        pres = float(incoming.get("pressure"))
    except (ValueError, TypeError):
        return "Invalid data format", 400

    ts = datetime.now()
    incoming["timestamp"] = ts
    data.append(incoming)

    x = {
        "temp": temp,
        "humidity": hum,
        "pressure": pres,
        **time_features(ts)
    }

    model.learn_one(x, temp)
    print(f"[{ts}] temp={temp}, hum={hum}, pres={pres}")

    return "OK", 200

@app.route("/")
def index():
    if not data:
        return "Nog geen data"

    last = data[-1]
    now = datetime.now()

    predictions = []
    temp = last["temperature"]

    for i in range(48):
        future_time = now + timedelta(hours=i + 1)

        x = {
            "temp": temp,
            "humidity": last["humidity"],
            "pressure": last["pressure"],
            **time_features(future_time)
        }

        temp = model.predict_one(x)
        predictions.append((future_time.strftime("%H:00"), temp))

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
  <h2>Aktuelle Messwerte</h2>
  <div class="metrics">
    <div class="metric">
      <span>Temperatur</span>
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
  <h2>Vorhersage (nächste 48 Stunden)</h2>
  <table>
    <tr>
      <th>Stunde</th>
      <th>Temperatur</th>
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
    return render_template_string(
        html,
        now=now.strftime("%d-%m-%Y %H:%M"),
        temp=last["temperature"],
        hum=last["humidity"],
        pres=last["pressure"],
        pred=predictions
    )

if __name__ == "__main__":
    print("Starting ML server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

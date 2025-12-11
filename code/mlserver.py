from flask import Flask, request, render_template_string
from river import linear_model, preprocessing
from datetime import datetime, timedelta

app = Flask(__name__)

data = []

model = preprocessing.StandardScaler() | linear_model.LinearRegression()

@app.route("/data", methods=["POST"])
def receive_data():
    incoming = request.get_json(force=True)
    if not incoming:
        return "No JSON received", 400

    try:
        temp = float(incoming.get("temperature", 0))
        hum  = float(incoming.get("humidity", 0))
        pres = float(incoming.get("pressure", 0))
    except (ValueError, TypeError):
        return "Invalid data format", 400

    incoming["timestamp"] = datetime.now()
    data.append(incoming)

    x = {"temp": temp, "humidity": hum, "pressure": pres}
    model.learn_one(x, temp)

    print(f"[{datetime.now()}] Received: temp={temp}, hum={hum}, pres={pres}")

    return "OK", 200

@app.route("/")
def index():
    if not data:
        return "Nog geen Data"

    last = data[-1]

    predictions = []
    x = {"temp": last["temperature"], "humidity": last["humidity"], "pressure": last["pressure"]}
    now = datetime.now()
    for i in range(48):
        pred_temp = model.predict_one(x)
        predictions.append((now + timedelta(hours=i+1), pred_temp))
        x["temp"] = pred_temp

    html = """
    <h1>Weerstation Zwaag</h1>
    <h2>Actuele meetingen</h2>
    <p>Temperatuur: {{ temp }} °C<br>
       Luchtvochtigheid: {{ hum }} %<br>
       Luchtdrukte: {{ pres }} hPa</p>

    <h2>Het weer in de volgende 48 uur</h2>
    <table border="1" cellpadding="5">
      <tr><th>Tijd</th><th>Temperatuur (°C)</th></tr>
      {% for t, p in pred %}
      <tr><td>{{ t }}</td><td>{{ p|round(2) }}</td></tr>
      {% endfor %}
    </table>
    """
    return render_template_string(html,
                                  temp=last["temperature"],
                                  hum=last["humidity"],
                                  pres=last["pressure"],
                                  pred=predictions)

if __name__ == "__main__":
    print("Starting ML server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)


#!/usr/bin/env python3

import os
import subprocess
import time

# CONFIG
PROJECT_DIR = os.path.expanduser("~/esp_project")
VENV_ACTIVATE = os.path.join(PROJECT_DIR, "venv", "bin", "activate")
URL = "http://192.168.2.26:5000"  # die aktuelle IP deines Laptops
TARGET_FOLDER = os.path.expanduser("~/Desktop/resultaten")
BROWSER_PATH = "/usr/bin/firefox"

# ensure folder exists
os.makedirs(TARGET_FOLDER, exist_ok=True)

# 1. Start ML server mit aktivierter venv
subprocess.Popen(["/bin/bash", "-c", f'source {VENV_ACTIVATE} && python3 mlserver.py'], cwd=PROJECT_DIR)
print("ML-Server booted, wacht 70 seconden")
time.sleep(70)

# 2. Öffne Webseite in Firefox
subprocess.Popen([BROWSER_PATH, URL])

# 3. Download-Loop (täglich)
import datetime
import requests

def next_free_filename():
    i = 1
    while True:
        path = os.path.join(TARGET_FOLDER, f"{i}.html")
        if not os.path.exists(path):
            return path
        i += 1

while True:
    try:
        # Website abrufen
        r = requests.get(URL, timeout=10)
        filename = next_free_filename()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"Nieuwe update:{filename}")
    except Exception as e:
        print(f"download error: {e}")

    # 24 Stunden warten
    time.sleep(24*3600)


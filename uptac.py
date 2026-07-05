import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://uptac.samarth.edu.in/index.php/notifications/index"

TELEGRAM_TOKEN = "8859699461:AAHQ_bOI5by8PkuMOO37Lacy2u3HSU0dLss"
CHAT_ID = "93372553"

DATA_FILE = "last.json"

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass

def get_data():
    try:
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        if not table:
            return []

        notices = []

        for row in table.find_all("tr"):
            text = row.get_text(" ", strip=True)

            if text and len(text) > 30 and "Published" not in text:
                notices.append(text)

        return notices

    except:
        return []

def load_old():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
    except:
        return []
    return []

def save_new(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

def run():
    new = get_data()
    old = load_old()

    if not old:
        save_new(new)
        send("UPTAC Monitor Started ✅")
        return

    changes = [x for x in new if x not in old]

    if changes:
        for c in changes:
            send("🔔 NEW UPTAC NOTICE:\n\n" + c)

    save_new(new)

run()

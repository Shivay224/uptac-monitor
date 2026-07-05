import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib

URL = "https://uptac.samarth.edu.in/index.php/notifications/index"

TELEGRAM_TOKEN = "8942906921:AAGkNJCxt2SfzBBp-ppaYAPHLAorojNypFo"
CHAT_ID = "8699041887"

DATA_FILE = "last.json"


# ---------- Telegram ----------
def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass


# ---------- Scrape UPTAC ----------
def get_data():
    try:
        r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        if not table:
            return []

        notices = []
        for row in table.find_all("tr"):
            text = row.get_text(" ", strip=True)

            # filter header + noise
            if text and len(text) > 30 and "Published" not in text:
                notices.append(text)

        return notices

    except:
        return []


# ---------- Load old state ----------
def load_old():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ---------- Save state ----------
def save_new(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ---------- Hash helper ----------
def hash_list(data):
    return set(hashlib.md5(x.encode()).hexdigest() for x in data)


# ---------- MAIN ----------
def run():
    new_data = get_data()
    old_data = load_old()

    new_hash = hash_list(new_data)
    old_hash = hash_list(old_data)

    # first run
    if not old_data:
        send("🚨 UPTAC Monitor Activated")
        save_new(new_data)
        return

    # detect new notices
    changes = [
        x for x in new_data
        if hashlib.md5(x.encode()).hexdigest() not in old_hash
    ]

    # send alerts
    for c in changes:
        send("🔔 NEW UPTAC NOTICE:\n\n" + c)

    save_new(new_data)


run()

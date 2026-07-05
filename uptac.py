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
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
        print("Telegram:", r.status_code, r.text)
    except Exception as e:
        print("Telegram Error:", e)


# ---------- Scraper (more stable) ----------
def get_data():
    try:
        r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.select("table tr")

        notices = []
        for row in rows:
            text = row.get_text(" ", strip=True)

            if text and len(text) > 25 and "Published" not in text:
                notices.append(text)

        return notices

    except Exception as e:
        print("Scraper Error:", e)
        return []


# ---------- Load ----------
def load_old():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ---------- Save ----------
def save_new(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ---------- Hash ----------
def make_hash(data):
    return set(hashlib.md5(x.encode()).hexdigest() for x in data)


# ---------- MAIN ----------
def run():
    new_data = get_data()
    old_data = load_old()

    new_hash = make_hash(new_data)
    old_hash = make_hash(old_data)

    # First run
    if not old_data:
        send("🚨 UPTAC Monitor Activated Successfully")
        save_new(new_data)
        return

    # Detect changes safely
    changes = [x for x in new_data if hashlib.md5(x.encode()).hexdigest() not in old_hash]

    if changes:
        for c in changes:
            send("🔔 NEW UPTAC NOTICE:\n\n" + c)

    save_new(new_data)


run()

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


# ---------- Get clean notices ----------
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

            # filter noise
            if text and len(text) > 25 and "Published" not in text:
                notices.append(text)

        return notices

    except Exception as e:
        print("Scraper Error:", e)
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


# ---------- Hash for stability ----------
def make_hash_list(data):
    return [hashlib.md5(x.encode()).hexdigest() for x in data]


# ---------- Main ----------
def run():
    new_data = get_data()
    old_data = load_old()

    new_hash = make_hash_list(new_data)
    old_hash = make_hash_list(old_data)

    # First run
   if not old:
    send("🚨 UPTAC Monitor Activated Successfully")
    save_new(new)

    # Find new items
    changes = []
    for i, h in enumerate(new_hash):
        if h not in old_hash:
            changes.append(new_data[i])

    if changes:
        for c in changes:
            send("🔔 NEW UPTAC NOTICE:\n\n" + c)

    save_new(new_data)


run()

import requests
from bs4 import BeautifulSoup
import os
import json
import hashlib

URL = "https://uptac.samarth.edu.in/index.php/notifications/index"
DATA_FILE = "last.json"

TELEGRAM_TOKEN = os.getenv("8942906921:AAGkNJCxt2SfzBBp-ppaYAPHLAorojNypFo")
CHAT_ID = os.getenv("8699041887")


# ---------- Telegram ----------
def send(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials")
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)


# ---------- Scrape ----------
def get_data():
    try:
        r = requests.get(
            URL,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        if not table:
            return []

        notices = []

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue

            text = " | ".join(c.get_text(strip=True) for c in cols)

            if len(text) > 10:
                notices.append(text)

        return notices

    except Exception as e:
        print("Scraping error:", e)
        return []


# ---------- File handling ----------
def load_old():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_new(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ---------- Hash ----------
def make_hash(data):
    return set(hashlib.sha256(x.encode()).hexdigest() for x in data)


# ---------- Main ----------
def run():
    new_data = get_data()
    old_data = load_old()

    if not new_data:
        print("No data found")
        return

    new_hash = make_hash(new_data)
    old_hash = make_hash(old_data)

    # first run
    if not old_data:
        send("🚨 UPTAC Monitor Activated")
        save_new(new_data)
        return

    # detect changes
    changes = [
        x for x in new_data
        if hashlib.sha256(x.encode()).hexdigest() not in old_hash
    ]

    if changes:
        for c in changes:
            send("🔔 NEW UPTAC NOTICE:\n\n" + c)

    save_new(new_data)


if __name__ == "__main__":
    run()

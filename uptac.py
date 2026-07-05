import requests
from bs4 import BeautifulSoup
import os
import json

URL = "https://uptac.samarth.edu.in/index.php/notifications/index"

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

FILE = "last.json"


# ---------- Telegram ----------
def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)


# ---------- Load state ----------
def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ---------- Save state ----------
def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- Scraper (ROBUST) ----------
def fetch():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        notices = []

        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            title = cols[0].get_text(" ", strip=True)
            published = cols[1].get_text(" ", strip=True)

            link_tag = cols[2].find("a")
            link = link_tag["href"] if link_tag else URL

            # filter junk rows
            if title and len(title) > 5:
                notices.append({
                    "title": title,
                    "published": published,
                    "link": link
                })

        return notices

    except Exception as e:
        print("Fetch error:", e)
        return []


# ---------- MAIN ----------
old = load()
new = fetch()

old_links = {i.get("link") for i in old if i.get("link")}

# ---------- FIRST RUN ----------
if not old:
    send("🚨 UPTAC MONITOR ACTIVATED\n\n📡 Sending current notices snapshot...")

    for n in new:
        send(
            f"📢 NOTICE\n\n"
            f"📌 {n['title']}\n"
            f"🕒 {n['published']}\n\n"
            f"🔗 {n['link']}"
        )

    save(new)
    exit()


# ---------- NORMAL RUN ----------
for n in new:
    if n["link"] not in old_links:
        send(
            "🚨 NEW NOTICE\n\n"
            f"📌 {n['title']}\n"
            f"🕒 {n['published']}\n\n"
            f"🔗 {n['link']}"
        )

save(new)

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
    except:
        pass


# ---------- Load memory ----------
def load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE, "r"))
    except:
        return []


# ---------- Save memory ----------
def save(data):
    json.dump(data, open(FILE, "w"), indent=2)


# ---------- Scrape ----------
def fetch():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        if not table:
            return []

        notices = []

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            title = cols[0].get_text(strip=True)
            published = cols[1].get_text(strip=True)

            link_tag = cols[2].find("a")
            link = link_tag["href"] if link_tag else URL

            notices.append({
                "title": title,
                "published": published,
                "link": link
            })

        return notices

    except:
        return []


# ---------- MAIN ----------
old = load()

# SAFE SET (this is correct way)
old_links = {i["link"] for i in old if "link" in i}

new = fetch()

# first run
if not old:
    send("🚨 UPTAC MONITOR ACTIVATED")
    save(new)
    exit()

# detect new notices
for n in new:
    if n["link"] not in old_links:

        msg = (
            "🚨 NEW UPTAC NOTICE\n\n"
            f"📌 {n['title']}\n"
            f"🕒 {n['published']}\n\n"
            f"🔗 {n['link']}"
        )

        send(msg)

# update memory
save(new)

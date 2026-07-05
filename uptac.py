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


# ---------- load ----------
def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ---------- save ----------
def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- scrape ----------
def fetch():
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


# ---------- MAIN ----------
old = load()
new = fetch()

old_links = {i["link"] for i in old if "link" in i}

# 🔥 FIRST RUN (FORCE SHOW ALL)
if not old:
    send("🚨 UPTAC MONITOR ACTIVATED\n\n📡 Sending current notices snapshot...")

    for n in new:
        msg = f"""📢 NOTICE

📌 {n['title']}
🕒 {n['published']}

🔗 {n['link']}"""
        send(msg)

    save(new)
    exit()


# 🔥 NORMAL RUN (ONLY NEW)
for n in new:
    if n["link"] not in old_links:

        msg = f"""🚨 NEW NOTICE

📌 {n['title']}
🕒 {n['published']}

🔗 {n['link']}"""

        send(msg)

save(new)

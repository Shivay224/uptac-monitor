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


# ---------- scrape ----------
def fetch():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table")
    if not table:
        return []

    data = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        title = cols[0].get_text(strip=True)
        published = cols[1].get_text(strip=True)

        link_tag = cols[2].find("a")
        link = link_tag["href"] if link_tag else URL

        data.append({
            "title": title,
            "published": published,
            "link": link
        })

    return data


# ---------- load ----------
def load():
    try:
        return json.load(open(FILE))
    except:
        return []


# ---------- save ----------
def save(data):
    json.dump(data, open(FILE, "w"), indent=2)


# ---------- main ----------
new = fetch()
old = load()

if not old:
    send("🚨 UPTAC MONITOR ACTIVATED (1-min mode)")
    save(new)
    exit()

old_links = {i["link"] for i in old}

for n in new:
    if n["link"] not in old_links:
        msg = f"""🚨 NEW NOTICE

📌 {n['title']}
🕒 {n['published']}

🔗 {n['link']}"""
        send(msg)

save(new)

import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://uptac.samarth.edu.in/index.php/notifications/index"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

seen = set()


# ---------- send telegram ----------
def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass


# ---------- fetch notices ----------
def fetch():
    try:
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
            link = link_tag["href"] if link_tag else None

            if title and link:
                data.append((title, published, link))

        return data

    except:
        return []


# ---------- main loop ----------
while True:
    notices = fetch()

    for title, published, link in notices:
        if link not in seen:
            seen.add(link)

            msg = (
                "🚨 NEW UPTAC NOTICE\n\n"
                f"📌 {title}\n"
                f"🕒 {published}\n\n"
                f"🔗 {link}"
            )

            send(msg)

    time.sleep(20)  # check every 20 seconds (safe + fast)

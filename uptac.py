import os
import json
import requests
from playwright.sync_api import sync_playwright

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


# ---------- load/save ----------
def load():
    try:
        return json.load(open(FILE))
    except:
        return []


def save(data):
    json.dump(data, open(FILE, "w"), indent=2)


# ---------- PLAYWRIGHT SCRAPER ----------
def fetch():
    notices = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)

        rows = page.locator("tr")
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            cols = row.locator("td")

            if cols.count() < 3:
                continue

            title = cols.nth(0).inner_text().strip()
            published = cols.nth(1).inner_text().strip()

            link_el = cols.nth(2).locator("a")

            link = URL
            if link_el.count() > 0:
                link = link_el.get_attribute("href")

            if title and len(title) > 5:
                notices.append({
                    "title": title,
                    "published": published,
                    "link": link
                })

        browser.close()

    return notices


# ---------- MAIN ----------
old = load()
new = fetch()

old_links = {i.get("link") for i in old if i.get("link")}

# FIRST RUN
if not old:
    send("🚨 UPTAC MONITOR ACTIVATED (Playwright Mode)")

    for n in new:
        send(
            f"📢 NOTICE\n\n"
            f"📌 {n['title']}\n"
            f"🕒 {n['published']}\n\n"
            f"🔗 {n['link']}"
        )

    save(new)
    exit()

# NORMAL RUN
for n in new:
    if n["link"] not in old_links:
        send(
            f"🚨 NEW NOTICE\n\n"
            f"📌 {n['title']}\n"
            f"🕒 {n['published']}\n\n"
            f"🔗 {n['link']}"
        )

save(new)

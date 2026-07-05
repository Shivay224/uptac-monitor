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
    except Exception as e:
        print("Telegram error:", e)


# ---------- Load / Save ----------
def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- PLAYWRIGHT SCRAPER ----------
def fetch():
    notices = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait full JS rendering
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)

        # capture possible notice elements (robust selector set)
        items = page.locator("a, .card, .container-fluid div, li, tr")

        seen = set()
        count = items.count()

        for i in range(count):
            el = items.nth(i)
            text = el.inner_text().strip()

            if len(text) < 15:
                continue

            link = URL
            try:
                href = el.get_attribute("href")
                if href:
                    link = href
            except:
                pass

            if text in seen:
                continue
            seen.add(text)

            notices.append({
                "title": text,
                "published": "",
                "link": link
            })

        browser.close()

    return notices


# ---------- MAIN ----------
old = load()
new = fetch()

old_links = {i.get("link") for i in old if i.get("link")}


# ---------- FIRST RUN ----------
if not old:
    send("🚨 UPTAC MONITOR ACTIVATED (Playwright Mode)\n📡 Sending current snapshot...")

    for n in new:
        send(
            "📢 NOTICE\n\n"
            f"📌 {n['title']}\n\n"
            f"🔗 {n['link']}"
        )

    save(new)
    exit()


# ---------- NORMAL RUN ----------
for n in new:
    if n["link"] not in old_links:
        send(
            "🚨 NEW UPTAC NOTICE\n\n"
            f"📌 {n['title']}\n\n"
            f"🔗 {n['link']}"
        )

save(new)

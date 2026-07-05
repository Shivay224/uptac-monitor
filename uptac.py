import requests

TELEGRAM_TOKEN = "YOUR_TOKEN"
CHAT_ID = "8699041888"

def send(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10
    )
    print(r.status_code)
    print(r.text)

send("🔥 TEST 1: GitHub → Telegram working?")

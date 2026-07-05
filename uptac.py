import requests

TELEGRAM_TOKEN = "8942906921:AAGkNJCxt2SfzBBp-ppaYAPHLAorojNypFo"
CHAT_ID = "8699041887"

def send(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10
    )
    print(r.status_code)
    print(r.text)

send("🔥 TEST 1: GitHub → Telegram working?")

import requests

TELEGRAM_TOKEN = "8942906921:AAGkNJCxt2SfzBBp-ppaYAPHLAorojNypFo"
CHAT_ID = "8699041887"

print("SCRIPT STARTED")

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

r = requests.post(
    url,
    data={"chat_id": CHAT_ID, "text": "🔥 GITHUB FINAL TELEGRAM TEST"},
    timeout=10
)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)

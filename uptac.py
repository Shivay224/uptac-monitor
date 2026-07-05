import requests

TELEGRAM_TOKEN = "8942906921:AAGkNJCxt2SfzBBp-ppaYAPHLAorojNypFo"
CHAT_ID = "8699041887"

print("STARTING SCRIPT")

r = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": "🚨 GitHub Actions FINAL TEST"},
    timeout=10
)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)

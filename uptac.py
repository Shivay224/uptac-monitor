print("SCRIPT STARTED")

import requests

r = requests.get("https://api.telegram.org")
print("Telegram reachable:", r.status_code)

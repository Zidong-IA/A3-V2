"""Configura el webhook de Telegram apuntando al dominio de Render."""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SECRET = os.environ["TELEGRAM_WEBHOOK_SECRET"]
DOMAIN = os.environ.get("RENDER_EXTERNAL_URL") or sys.argv[1] if len(sys.argv) > 1 else None

if not DOMAIN:
    print("Uso: python tools/scripts/set_webhook.py https://tu-app.onrender.com")
    sys.exit(1)

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
payload = {
    "url": f"{DOMAIN.rstrip('/')}/webhook",
    "secret_token": SECRET,
    "allowed_updates": ["message"],
}

resp = requests.post(url, json=payload, timeout=10)
data = resp.json()

if data.get("ok"):
    print(f"Webhook configurado: {payload['url']}")
else:
    print(f"Error: {data}")
    sys.exit(1)

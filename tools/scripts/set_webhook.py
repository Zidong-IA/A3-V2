"""Configura el webhook de Telegram apuntando al dominio activo (Render o ngrok)."""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SECRET = os.environ["TELEGRAM_WEBHOOK_SECRET"]

# Prioridad: argumento CLI → variable de entorno → ngrok_url.txt
def _get_domain() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    if os.environ.get("RENDER_EXTERNAL_URL"):
        return os.environ["RENDER_EXTERNAL_URL"]
    url_file = Path(__file__).parent / "ngrok_url.txt"
    if url_file.exists():
        for line in url_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
    return None

DOMAIN = _get_domain()

if not DOMAIN or "TU-URL" in DOMAIN:
    print("ERROR: no hay URL configurada.")
    print("Opciones:")
    print("  1. Editá tools/scripts/ngrok_url.txt con tu URL de ngrok")
    print("  2. Pasala como argumento: python set_webhook.py https://tu-url.ngrok.io")
    print("  3. Seteá RENDER_EXTERNAL_URL en el .env")
    sys.exit(1)

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
payload = {
    "url": f"{DOMAIN.rstrip('/')}/webhooks/telegram",
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

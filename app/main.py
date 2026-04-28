from flask import Flask, request, jsonify, abort
from app.config import TELEGRAM_WEBHOOK_SECRET, FLASK_SECRET_KEY
from app.agent import process_turn
from app.services import telegram

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY


@app.route("/webhooks/telegram", methods=["POST"])
def telegram_webhook():
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if token != TELEGRAM_WEBHOOK_SECRET:
        abort(403)

    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message") or data.get("edited_message")

    if not message or "text" not in message:
        return jsonify({"ok": True})

    chat_id = str(message["chat"]["id"])
    user_text = message["text"]

    try:
        reply = process_turn(chat_id, user_text)
    except Exception as e:
        app.logger.error("Error processing turn for %s: %s", chat_id, e, exc_info=True)
        reply = "Disculpa, tuve un problema interno. Ya le avisé al equipo. Por favor intenta de nuevo en un momento."

    try:
        telegram.send_message(chat_id, reply)
    except Exception as e:
        app.logger.error("Error sending message to %s: %s", chat_id, e)

    return jsonify({"ok": True})


@app.route("/setup-webhook", methods=["POST"])
def setup_webhook():
    from app.config import TELEGRAM_WEBHOOK_URL, TELEGRAM_WEBHOOK_SECRET
    result = telegram.set_webhook(TELEGRAM_WEBHOOK_URL, TELEGRAM_WEBHOOK_SECRET)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

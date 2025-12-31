from flask import Flask, request, jsonify
from config import *
from limiter import load_state, save_state, can_send, mark_sent
from formatter import format_signal
from services.telegram import send_message

app = Flask(__name__)

@app.route("/tv", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"ok": False, "error": "no json"}), 400

    if data.get("type") != "MSB_OB_BUY":
        return jsonify({"ok": True, "skip": "not buy signal"}), 200

    if data.get("tf") != ALLOWED_TIMEFRAME:
        return jsonify({"ok": True, "skip": "wrong timeframe"}), 200

    key = f"{data['symbol']}|{data['tf']}|MSB_OB"

    state = load_state()
    if not can_send(state, key, MAX_SIGNALS_PER_MINUTE, DEDUP_HOURS):
        return jsonify({"ok": True, "skip": "rate/dedup"}), 200

    message = format_signal(data)
    send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

    mark_sent(state, key)
    save_state(state)

    return jsonify({"ok": True, "sent": True}), 200

@app.route("/", methods=["GET"])
def health():
    return "MSB-OB Bot is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

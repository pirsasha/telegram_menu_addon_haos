
from flask import Flask, request, jsonify, send_file
import yaml
import os

app = Flask(__name__)

MENU_CONFIG_PATH = "/share/telegram_menu_config.yaml"
AUTOMATIONS_OUTPUT_PATH = "/share/generated_telegram_automations.yaml"

@app.route("/api/save_menu", methods=["POST"])
def save_menu():
    data = request.json
    with open(MENU_CONFIG_PATH, "w") as f:
        yaml.dump(data, f, allow_unicode=True)
    return {"status": "saved"}

@app.route("/api/generate_automations", methods=["POST"])
def generate_automations():
    data = request.json
    automations = []

    for room in data.get("rooms", []):
        command = f"/{room['slug']}_control"
        automation = {
            "id": f"telegram_{room['slug']}_menu",
            "alias": f"Telegram меню - {room['name']}",
            "trigger": [
                {"platform": "event", "event_type": "telegram_callback", "event_data": {"command": command}}
            ],
            "action": [
                {"service": "telegram_bot.send_message",
                 "data": {
                     "target": "{{ trigger.event.data.chat_id }}",
                     "message": f"\U0001F4CB Меню управления - {room['name']}",
                     "inline_keyboard": [
                         f"{device['icon']} {device['name']}:/{device['command']}"
                         for device in room.get("devices", [])
                     ]
                 }}
            ]
        }
        automations.append(automation)

    with open(AUTOMATIONS_OUTPUT_PATH, "w") as f:
        yaml.dump(automations, f, allow_unicode=True)

    return {"status": "generated"}

@app.route("/api/download_yaml", methods=["GET"])
def download_yaml():
    return send_file(AUTOMATIONS_OUTPUT_PATH, as_attachment=True)

@app.route("/api/ping")
def ping():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8123)


from flask import send_from_directory

@app.route("/")
def serve_ui():
    return send_from_directory("/app/web", "index.html")

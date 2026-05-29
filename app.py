from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
CREDS_FILE = "credentials.json"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        if data and data.get("data") and data["data"][0]:
            d = data["data"][0]
            creds = {
                "APP_KEY":    d.get("appKey", ""),
                "APP_SECRET": d.get("appSecret", ""),
                "CLIENT_ID":  d.get("clientId", ""),
                "ROUTER_URL": d.get("domain", ""),
            }
            with open(CREDS_FILE, "w") as f:
                json.dump(creds, f)
            print(f"[Webhook] Zapisano: {creds['APP_KEY']}")
    except Exception as e:
        print(f"[Webhook] Błąd: {e}")
    return "ok", 200

@app.route("/credentials", methods=["GET"])
def credentials():
    try:
        with open(CREDS_FILE) as f:
            return jsonify(json.load(f))
    except:
        return jsonify({}), 200

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

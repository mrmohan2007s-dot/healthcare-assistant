import os
import json
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# load .env from backend folder if present
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from backend import llm_handler, safety_filter
from backend.config import CONFIG

static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app = Flask(__name__, static_folder=static_folder, static_url_path="")


@app.route("/", methods=["GET"])
def home():
    # Serve frontend index.html when available; otherwise return a simple status JSON.
    try:
        return app.send_static_file("index.html")
    except Exception:
        return jsonify({"status": "ok", "service": "Smart Health Assistant (non-diagnostic)"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing 'query' in JSON body"}), 400

    allowed, reason = safety_filter.check_query(query)
    disclaimer = safety_filter.get_disclaimer()
    if not allowed:
        return jsonify({"disclaimer": disclaimer, "refused": True, "reason": reason}), 403

    try:
        resp = llm_handler.generate_response(query)
    except Exception as e:
        return jsonify({"error": "internal_error", "message": str(e)}), 500

    resp.setdefault("disclaimer", disclaimer)
    return jsonify(resp)


@app.route("/faq", methods=["GET"])
def faq():
    # Serve basic FAQ data from the data directory to the frontend
    try:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        path = os.path.join(data_dir, "faq.json")
        with open(path, "r", encoding="utf-8") as fh:
            return jsonify(json.load(fh))
    except Exception:
        return jsonify([])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "1") in ("1", "true", "True")
    app.run(host="0.0.0.0", port=port, debug=debug)

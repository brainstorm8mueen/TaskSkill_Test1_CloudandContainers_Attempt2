import logging, os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
ENVIRONMENT = os.getenv("APP_ENV", "production")
SERVICE_NAME = os.getenv("SERVICE_NAME", "production-backend")
tickets = [{"id": 1, "title": "Verify development deployment", "status": "Open", "environment": ENVIRONMENT}]

@app.get("/")
def index(): return jsonify(service=SERVICE_NAME, environment=ENVIRONMENT, status="running")
@app.get("/health")
def health(): return jsonify(status="healthy", service=SERVICE_NAME)
@app.get("/api/tickets")
def get_tickets(): return jsonify(environment=ENVIRONMENT, tickets=tickets, timestamp=datetime.now(timezone.utc).isoformat())
@app.post("/api/tickets")
def create_ticket():
    data = request.get_json(silent=True) or {}
    if not str(data.get("title", "")).strip(): return jsonify(error="title is required"), 400
    ticket = {"id": len(tickets)+1, "title": data["title"].strip(), "status": "Open", "environment": ENVIRONMENT}
    tickets.append(ticket); app.logger.info("Created ticket %s", ticket["id"])
    return jsonify(ticket), 201
@app.errorhandler(404)
def not_found(_): return jsonify(error="endpoint not found"), 404

if __name__ == "__main__": app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3002")), debug=os.getenv("FLASK_DEBUG") == "1")

from flask import Flask, jsonify, request
app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/users")
def get_users():
    return jsonify(users)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    if username:
        return jsonify({"message": f"Welcome {username}"})
    return jsonify({"error": "username required"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosemgrep: python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host
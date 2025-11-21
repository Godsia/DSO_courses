"""Simple web application for containerization demo."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "secure-app"})


@app.route("/api/info")
def info():
    """Application info endpoint."""
    return jsonify({
        "name": "Secure Coding App",
        "version": "1.0.0",
        "description": "Secure coding practices demonstration"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


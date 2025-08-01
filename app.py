from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_valid_email(email):
    # Basic regex check
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email) is not None

def is_disposable(email):
    disposable_domains = ["mailinator.com", "tempmail.com", "10minutemail.com"]
    domain = email.split("@")[-1]
    return domain in disposable_domains

@app.route("/validate_email", methods=["POST"])
def validate_email():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    if not is_valid_email(email):
        return jsonify({"status": "Invalid", "message": "Invalid email format"})

    if is_disposable(email):
        return jsonify({"status": "Disposable", "email": email})
    else:
        return jsonify({"status": "Valid", "email": email})

import os
import json
import uuid
from flask import Blueprint, request, jsonify

USER_DATA_FILE = "data/users.json"

auth_bp = Blueprint('auth', __name__)

def read_json_file(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def write_json_file(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"msg": "Name, email, and password are required"}), 400

    users = read_json_file(USER_DATA_FILE)
    if any(user["email"] == email for user in users):
        return jsonify({"msg": "Email already in use"}), 400

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": password
    }
    users.append(new_user)
    write_json_file(USER_DATA_FILE, users)

    return jsonify({"msg": "User created", "user_id": new_user["id"]}), 201

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"msg": "Email and password are required"}), 400

    users = read_json_file(USER_DATA_FILE)
    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    return jsonify({"msg": "Login successful", "user_id": user["id"]}), 200

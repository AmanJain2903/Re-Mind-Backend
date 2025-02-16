import os
import json
from flask import Blueprint, request, jsonify

questions_bp = Blueprint('questions', __name__)

# Define the file to store user responses
RESPONSES_FILE = "data/user_responses.json"

# Helper functions to read and write JSON files
def read_json_file(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as file:
        return json.load(file)

def write_json_file(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

# Endpoint to get a list of questions
@questions_bp.route('/get_questions', methods=['GET'])
def get_questions():
    questions = {
        "How do you feel today?": "0",
        "What was the most challenging part of your day?": "0",
        "What made you smile today?": "0",
        "What was your most productive moment?": "0",
        "What was your biggest distraction today?": "0",
        "What is one thing you’re grateful for?": "0",
        "What is one thing you learned today?": "0",
        "What could have gone better?": "0",
        "How do you feel about tomorrow?": "0",
        "What is one thing you’ll do differently tomorrow?": "0"
    }
    return jsonify(questions)

# Endpoint to submit responses to questions
@questions_bp.route('/submit', methods=['POST'])
def submit_questions():
    data = request.get_json()
    user_id = data.get('user_id')
    responses = data.get('responses') 

    # Load existing responses from the JSON file
    all_responses = read_json_file(RESPONSES_FILE)

    # Add or update the user's responses
    all_responses[user_id] = responses

    # Save the updated responses back to the file
    write_json_file(RESPONSES_FILE, all_responses)

    return jsonify({"msg": "Responses submitted successfully"})

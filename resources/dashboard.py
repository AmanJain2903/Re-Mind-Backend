import os
import json
import uuid
from flask import Blueprint, request, jsonify
from threading import Thread


ENTRY_DATA_FILE = "data/entries.json"

dashboard_bp = Blueprint('dashboard', __name__)

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

@dashboard_bp.route('/entries', methods=['POST'])
def submit_entry():
    data = request.get_json()
    if not all(k in data for k in ["entryId", "date", "text", "user_id"]):
        return jsonify({"msg": "Missing required fields"}), 400

    entry = {
        "entry_id": data.get("entry_id"),
        "date": data.get("date"),
        "text": data.get("text"),
        "emotions": data.get("emotions"),
        "categories": data.get("categories"),
        "ai": None,  # Placeholder for the AI output
        "user_id": data.get("user_id")
    }
    
    from threading import Thread

    def run_ai():
        entry["ai"] = runMistral(entry["text"])
        entries = read_json_file(ENTRY_DATA_FILE)
        entries.append(entry)
        write_json_file(ENTRY_DATA_FILE, entries)

    Thread(target=run_ai).start()

    return jsonify({"msg": "Entry submission in progress"}), 202

@dashboard_bp.route('/entries', methods=['GET'])
def get_entries():
    user_id = request.args.get('user_id')
    entry_id = request.args.get('entry_id')

    
    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400

    
    entries = read_json_file(ENTRY_DATA_FILE)

    
    user_entries = [entry for entry in entries if entry.get("user_id") == user_id]


    if entry_id:
        filtered_entry = next((entry for entry in user_entries if entry.get("entry_id") == entry_id), None)
        
        if filtered_entry:
            return jsonify(filtered_entry), 200
        else:
            return jsonify({"msg": "Entry not found"}), 404

    return jsonify(user_entries), 200



systemPrompt = """

You are a Cognitive Behavioral Therapy (CBT)-based assistant designed to help users reframe their negative thoughts. Your task is to follow this structured format:  

1. Acknowledge the user's thoughts with empathy and validation.  
2. Identify and state the Cognitive Distortion present in the user's thoughts. Examples: Catastrophizing, Black-and-White Thinking, Overgeneralization, etc.  
3. Provide 2-3 reframing options to help the user shift their perspective in a healthier way. Ensure these options are practical and encouraging.  
4. Offer one actionable solution to address the user's concern. This should be simple, feasible, and supportive.  

Guidelines:  
- Keep responses between 150-250 words.  
- Maintain a compassionate, non-judgmental tone.  
- Use clear and concise language.  
- Do not dismiss the user's feelings; instead, help them see alternative viewpoints.  
- Ensure responses are emotionally supportive and solution-oriented.  

Example Output:  

User Input: "I failed my test. I'm never going to be good enough, and I'll probably fail in life too."  

Your Response:  
1. I hear that you're feeling disappointed and discouraged about your test results. It's understandable to feel this way.  
2. The cognitive distortion here is Overgeneralization—assuming that one failure defines your entire future.  
3. Let's reframe this:  
   - "This was one test. It doesn't define my abilities; I can learn and improve."  
   - "Many successful people have faced setbacks. This is an opportunity to grow."  
   - "I can analyze my mistakes and prepare better next time."  
4. A practical step you can take is to review what went wrong, create a better study plan, and seek help if needed. Progress comes from learning, not just from success.  

"""

CBTPrompt = {
    "system": systemPrompt,
    "temperature": 0.7,
    "top_p": 0.9
    }

def runMistral(prompt):
    command = f'echo \'{{"prompt":"{prompt}", "context": {json.dumps(CBTPrompt)}, "model":"mistral"}}\' | ollama run mistral'

    response = os.popen(
        command
    ).read()
    print(response)
    return response


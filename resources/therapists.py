from flask import Blueprint, request, jsonify,json
import random
therapists_bp = Blueprint('therapists', __name__)

@therapists_bp.route('/', methods=['GET'])
def get_therapists():
    with open('data/therapists.json', 'r') as file:
        therapists_list = json.load(file)
    random_therapists = random.sample(therapists_list, min(5, len(therapists_list)))

    return jsonify(random_therapists)

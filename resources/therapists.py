from flask import Blueprint, request, jsonify
therapists_bp = Blueprint('therapists', __name__)

@therapists_bp.route('/nearby', methods=['GET'])
def get_therapists():
    # For example, filter by location coordinates
    location = request.args.get('location')
    therapists = list(mongo.db.therapists.find({
        "location": {"$near": {"$geometry": {"type": "Point", "coordinates": [float(x) for x in location.split(',')]}}}
    }))
    return jsonify(therapists)

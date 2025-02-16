from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config
from resources.auth import auth_bp
from resources.questions import questions_bp
from resources.dashboard import dashboard_bp
from resources.therapists import therapists_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

USER_DATA_FILE = "data/users.json"
ENTRY_DATA_FILE = "data/entries.json"
THERAPISTS_DATA_FILE = "data/therapists.json"
THERAPISTS_DATA_FILE = "data/therapists.json"


def read_json_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as file:
        return json.load(file)

def write_json_file(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


mongo = PyMongo(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(questions_bp, url_prefix='/questions')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(therapists_bp, url_prefix='/therapists')



if __name__ == '__main__':
    app.run()

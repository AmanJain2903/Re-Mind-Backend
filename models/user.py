from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_user(name, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = mongo.db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    }).inserted_id
    return user_id

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/remind_ai')
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    DEBUG = True

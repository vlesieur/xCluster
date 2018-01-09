from flask import Flask
from flask_mongoengine import MongoEngine
from config import BaseConfig
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='storage')  
app.config.from_object(BaseConfig)
db = MongoEngine(app)
bcrypt = Bcrypt(app)
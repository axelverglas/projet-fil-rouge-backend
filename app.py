from flask import Flask
from db import mongo
from dotenv import load_dotenv
import os
from src.api.v1.routes.auth_routes import auth_blueprint
from src.api.v1.routes.user_routes import user_blueprint
from flask_cors import CORS
from src.socket_events import socketio
from src.api.v1.routes.game_routes import games_bp


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio.init_app(app, cors_allowed_origins="*") 

# Configuration de la base de données MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo.init_app(app)

@app.route('/')
def index():
    return "Hello World"

socketio.init_app(app, cors_allowed_origins="*")

app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(user_blueprint, url_prefix='/api/v1/user')
app.register_blueprint(games_bp, url_prefix='/api/v1/games')

if __name__ == "__main__":
    socketio.run(app, debug=True)
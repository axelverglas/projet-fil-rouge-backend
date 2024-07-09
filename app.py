from flask import Flask
from db import mongo
from dotenv import load_dotenv
import os
from src.api.v1.routes.auth_routes import auth_blueprint
from src.api.v1.routes.user_routes import user_blueprint
from flask_cors import CORS
from src.socket_events import socketio
from src.api.v1.routes.game_routes import games_bp
from src.api.v1.routes.friendship_routes import friendship_blueprint
import logging
import certifi

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio.init_app(app, cors_allowed_origins="*") 

# Configuration de la base de données MongoDB
mongo_uri = (
    f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
    f"@{os.getenv('MONGO_PATH')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority&tls=true&tlsCAFile={certifi.where()}"
)
app.config["MONGO_URI"] = mongo_uri
logger.debug(f"MONGO_URI: {app.config['MONGO_URI']}")
mongo.init_app(app)
logger.debug(f"MongoDB initialized: {mongo.db}")

@app.route('/')
def index():
    return "Hello World"
    

socketio.init_app(app, cors_allowed_origins="*")

app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(user_blueprint, url_prefix='/api/v1/user')
app.register_blueprint(friendship_blueprint, url_prefix='/api/v1/friendships')
app.register_blueprint(games_bp, url_prefix='/api/v1/games')

if __name__ == "__main__":
    socketio.run(app, debug=True)
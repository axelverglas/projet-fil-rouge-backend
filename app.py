from flask import Flask
from db import mongo
from dotenv import load_dotenv
import os
from src.api.v1.routes.auth_routes import auth_blueprint

load_dotenv()

app = Flask(__name__)

# Configuration de la base de données MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo.init_app(app)


@app.route('/')
def index():
    return "Hello, World!"


app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

if __name__ == "__main__":
    app.run(debug=True)
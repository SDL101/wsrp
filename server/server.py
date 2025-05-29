"""Server code consists of an API to access the database"""

# Import necessary libraries and modules
import re
from datetime import timedelta
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required
from extentions import db, limiter, csrf, jwt
from flask_cors import CORS
from sqlalchemy import text
from routes import register_blueprints
from routes.csrf_routes import csrf_bp
csrf.exempt(csrf_bp)
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Load JWT secret key from .env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres@localhost/banking_db_v0')
if not DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = 'postgresql://' + DATABASE_URL.split('://', 1)[1]
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {'connect_timeout': 10}
}

# JWT Configuration
app.config['JWT_COOKIE_SECURE'] = False  # This is so we can test locally (send token over http instead of https)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # allow JWT to be sent in cookies

# Enable Cross-Origin Resource Sharing to allow requests from different domains
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "supports_credentials": True
    }
})

# Initialize extensions
jwt.init_app(app)
db.init_app(app)
csrf.init_app(app)
limiter.init_app(app)

# Register blueprints
register_blueprints(app)

from routes.auth_routes import auth_bp
csrf.exempt(auth_bp)

# Configure Limiter to send JSON response instead of default Text/HTML
@app.errorhandler(429)
def ratelimit_handler(e):
    """Configure Limiter to send JSON response instead of default Text/HTML"""
    return make_response(
        jsonify(error=f"ratelimit exceeded {e.description}")
        , 429
    )

# Added root route
@app.route('/')
def home():
    """Returns a confirmation that the server is running"""
    return "Welcome to the Flask API!"

# Define a basic route to confirm the API is running
@app.route('/api')
def index():
    """Returns a confirmation that the API is running"""
    return "API is up and running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
import psycopg2
import os

# Initialize extensions without app
db = SQLAlchemy(engine_options={
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {'connect_timeout': 10},
    'creator': lambda: psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://postgres@localhost/banking_db_v0'))
})
jwt = JWTManager()
limiter = Limiter(get_remote_address)
csrf = CSRFProtect()

# Global state to track failed attempts
failed_attempts = {}


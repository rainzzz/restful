from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

redis = FlaskRedis()
db = SQLAlchemy()
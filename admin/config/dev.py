from . import BaseConfig

class DevConfig(BaseConfig):
    DEBUG = True
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = "postgresql://user:pwssword@127.0.0.1:5432/testdb"
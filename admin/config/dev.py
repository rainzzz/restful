from . import BaseConfig

class DevConfig(BaseConfig):
    DEBUG = True
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = 'postgresql://zhangyuwei:123456@127.0.0.1:5432/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
from . import BaseConfig

class DevConfig(BaseConfig):
    DEBUG = True
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = 'postgresql://zhangyuwei:123456@10.0.2.108:5432/yeyou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
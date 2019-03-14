import importlib
import json

from flask import Flask, make_response
from flask_restful import Api

from .common.error import ERRORS


def create_app(config_name):
    config_module = importlib.import_module(f'admin.config.{config_name}')
    config_obj = getattr(config_module, f"{config_name.capitalize()}Config")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    api = Api(app)
    if app.config['DEBUG']:
        api.errors = ERRORS

    # @api.representation('application/json')
    # def output_json(data, code, headers=None):
    #     resp = make_response(json.dumps(data), code)
    #     resp.headers.extend(headers or {})
    #     return resp

    # 初始化
    configure_extensions(app)
    configure_resource(api)
    return app


def configure_extensions(app):
    from .extensions import redis
    redis.init_app(app)


def configure_resource(api):
    from .route import routes

    for obj in routes:
        api.add_resource(obj.resource, *obj.urls, **obj.kwargs)

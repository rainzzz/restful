import importlib
from flask import abort

from flask import Flask, redirect
from flask_restful import Api
from flask_login import LoginManager

from admin.common.error import ERRORS


def create_app(config_name):
    config_module = importlib.import_module(f'admin.config.{config_name}')
    config_obj = getattr(config_module, f"{config_name.capitalize()}Config")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    api = Api(app, errors=ERRORS)
    # 初始化
    configure_extensions(app)
    configure_login(app)
    configure_resource(api)
    return app


def configure_login(app):
    from admin.models.staff import Staff
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Staff.query.filter(Staff.id == user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return abort(401)

    # login_manager.login_view = redirect(app.config['WEB_SITE'])
    login_manager.login_message = "未登录状态"


def configure_extensions(app):
    from .extensions import redis
    from .extensions import db
    redis.init_app(app)
    db.init_app(app)


def configure_resource(api):
    from .route import routes

    for obj in routes:
        api.add_resource(obj.resource, *obj.urls, **obj.kwargs)

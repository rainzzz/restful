from flask_restful import fields

class Resource:
    def __init__(self, resource, *urls, **kwargs):
        self.resource = resource
        self.urls = urls
        self.kwargs = kwargs


class Response:
    """
    统一响应格式
    """

    def __init__(self, code: int = 0, msg: str = 'ok', data=None):
        self.code = code
        self.msg = msg
        self.data = data or {}


def make_fields(data=None) -> dict:
    return {
        'code': fields.Integer,
        'msg': fields.String,
        'data': fields.Nested(data or {})
    }

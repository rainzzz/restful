import datetime

from flask import request
from flask_restful import Resource, fields
from flask_restful import reqparse, marshal_with
from flask_login import login_required, login_user, logout_user

from admin.common.utils import Response, make_fields
from admin.models.staff import Staff


class Login(Resource):
    """
    登陆
    """
    @marshal_with(make_fields({
        'id': fields.Integer,
        'zonst_id': fields.Integer,
        'realname': fields.String,
        'role_id': fields.Integer
    }))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login_name', location='json', type=str, required=True, help="缺少用户名")
        parser.add_argument('password', location='json', type=str, required=True, help="缺少密码")
        args = parser.parse_args()

        staff = Staff.query.rbac(**args)
        if staff:
            login_user(staff, remember=True, duration=datetime.timedelta(days=30))
            return Response(data=staff)
        return Response(-1, '账号密码错误')


class Logout(Resource):
    """
    注销登陆
    """
    @login_required
    @marshal_with(make_fields())
    def get(self):
        logout_user()
        return Response()

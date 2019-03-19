from flask import request
from flask_restful import Resource, fields
from flask_restful import reqparse, marshal_with
from flask_login import login_required, login_user, logout_user

from admin.common.utils import Response, make_fields
from admin.models.staff import Staff as StaffModel, StaffRole as StaffRoleModel
from admin.extensions import db


class Staff(Resource):
    """
    登陆人员接口
    post: 增加
    put: 修改
    get: 获取
    delete: 删除
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('zonst_id', location='json', type=int, required=True, help="缺少工号")
        self.parser.add_argument('realname', location='json', type=str, required=True)
        self.parser.add_argument('login_name', location='json', type=str, required=True)
        self.parser.add_argument('role_id', location='json', type=int, required=True)

    @marshal_with(make_fields({
        'id': fields.Integer
    }))
    @login_required
    def post(self):
        """增加"""
        parser = self.parser.copy()
        args = parser.parse_args()
        staff = StaffModel.query.filter(StaffModel.zonst_id == args.get('zonst_id')).first()
        if staff:
            return Response(code=-2, msg='数据已存在')
        staff = StaffModel(**args)
        db.session.add(staff)
        db.session.commit()
        return Response(data=staff)

    @marshal_with(make_fields({
        "id": fields.Integer
    }))
    @login_required
    def delete(self):
        """删除"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json', type=int, required=True)
        args = parser.parse_args()
        staff = StaffModel.query.filter(StaffModel.id == args.get('id')).first()
        if not staff:
            return Response(code=-2, msg='数据不存在')

        db.session.delete(staff)
        db.session.commit()
        return Response(data=staff)

    @marshal_with(make_fields({
        'id': fields.Integer
    }))
    @login_required
    def put(self):
        """修改"""
        parser = self.parser.copy()
        parser.add_argument('id', location='json', type=int, required=True)
        args = parser.parse_args()
        staff = StaffModel.query.filter(StaffModel.id == args.get('id')).first()
        if not staff:
            return Response(code=-2, msg='数据不存在')
        staff.realname = args.get('realname')
        staff.login_name = args.get('login_name')
        staff.role_id = args.get('role_id')
        db.session.commit()
        return Response(data=staff)

    @marshal_with(make_fields({
        'id': fields.Integer,
        'zonst_id': fields.Integer,
        'realname': fields.String,
        'role_id': fields.Integer
    }))
    @login_required
    def get(self):
        """查询"""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='args')
        args = parser.parse_args()
        objs = StaffModel.query
        if 'id' in args.keys() and args['id']:
            objs = objs.filter(StaffModel.id == args.get('id'))
        objs = objs.all()
        return Response(data=objs)


class StaffRole(Resource):
    """
    角色表
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('role_name', type=str, location='json')
        self.parser.add_argument('endpoints', type=str, action='append', location='json')

    @marshal_with(make_fields({
        "id": fields.Integer
    }))
    @login_required
    def post(self):
        parser = self.parser.copy()
        args = parser.parse_args()
        obj = StaffRoleModel.query.filter(StaffRoleModel.role_name == args.get('role_name')).first()
        if obj:
            return Response(code=-2, msg='角色名重复')
        obj = StaffRoleModel(**args)
        db.session.add(obj)
        db.session.commit()
        return Response(data=obj)

    @marshal_with(make_fields({
        "id": fields.Integer
    }))
    @login_required
    def put(self):
        parser = self.parser.copy()
        parser.add_argument("id", type=int, location='json', required=True)
        args = parser.parse_args()
        obj = StaffRoleModel.query.filter(StaffRoleModel.id == args.get('id')).first()
        if not obj:
            return Response(code=-2, msg='数据不存在')
        obj.role_name = args.get('role_name')
        obj.endpoints = args.get('endpoints')
        db.session.commit()
        return Response(data=obj)

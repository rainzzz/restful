from flask_restful import Resource, fields
from flask_restful import reqparse, marshal_with

from admin.common.utils import Response, make_fields


class Login(Resource):
    post_fields = make_fields({
        'id': fields.Integer
    })

    @marshal_with(post_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', type=str, required=True, help="缺少用户名")
        parser.add_argument('password', location='json', type=str, required=True, help="缺少密码")
        args = parser.parse_args()
        if args['username'] == args['password']:
            return Response(data=[{"id": 130}, {"id": 131}])
        return Response(-1, '账号密码错误')

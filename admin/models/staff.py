import datetime

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, Integer, ARRAY, VARCHAR, String, DateTime, text
from flask_login import UserMixin

from admin.extensions import db
from admin.interface.rbac import RBACLogin


class StaffQuery(BaseQuery):
    def rbac(self, login_name, password):
        rl = RBACLogin(login_name=login_name, password=password)
        user = rl.validate()
        if user:
            zonst_id = user.get('zonst_id')
            staff = self.filter(Staff.zonst_id == zonst_id).first()
            return staff
        return None


class Staff(UserMixin, db.Model):
    __tablename__ = 'staff_staff'
    query_class = StaffQuery

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zonst_id = db.Column(db.Integer)
    realname = db.Column(db.String(20), nullable=False)
    login_name = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class StaffRole(db.Model):
    __tablename__ = 'staff_role'

    id = Column(Integer, primary_key=True, server_default=text("nextval('staff_role_id_seq'::regclass)"))
    role_name = Column(String(20), nullable=False, server_default=text("'default'::character varying"))
    endpoints = Column(ARRAY(VARCHAR()), nullable=False, server_default=text("'{}'::character varying[]"))
    create_time = Column(DateTime, nullable=False, server_default=text("now()"))

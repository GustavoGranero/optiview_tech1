from flask_login import UserMixin
from sqlalchemy.sql import func

from optview import db
from models.base_mixin import BaseMixin


class Users(UserMixin, BaseMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    full_name = db.Column(db.String(250), unique=True, nullable=False)   
    email = db.Column(db.String(250), unique=True, nullable=False)
    hash_type_id = db.Column(db.Integer, db.ForeignKey('hash_types.id'), unique=False, nullable=False, default=1)
    hash = db.Column(db.LargeBinary, unique=False, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), unique=False, nullable=False, default=1)
    phone = db.Column(db.String(250), unique=False, nullable=False)
    verified = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    login_failure_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    login_failure_timestamp = db.Column(db.DateTime, unique=False, nullable=True, default=None)

    plan = db.relationship('Plans', backref='users', lazy='joined')
    hash_type = db.relationship('HashTypes', backref='users', lazy='joined')


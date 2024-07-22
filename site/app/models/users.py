from flask_login import UserMixin

from optview import db


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    hash_type = db.Column(db.Integer, unique=False, nullable=False)
    hash = db.Column(db.LargeBinary, unique=False, nullable=False)
    plan_id = db.Column(db.Integer, unique=False, nullable=False)
    phone = db.Column(db.String(250), unique=False, nullable=False)
    login_failure_count = db.Column(db.Integer, unique=False, nullable=False)
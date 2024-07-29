
from flask_login import UserMixin

from optview import db


class Plans(UserMixin, db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, db.ForeignKey('users.plan_id'), primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
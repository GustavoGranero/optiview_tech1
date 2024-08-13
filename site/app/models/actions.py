from sqlalchemy.sql import func

from optview import db
from models.base_mixin import BaseMixin


class Actions(BaseMixin, db.Model):
    __tablename__ = "actions"

    id = db.Column(db.Integer, primary_key=True)
    action_type_id = db.Column(db.Integer, db.ForeignKey('action_types.id'), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    token = db.Column(db.String(250), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, default=func.now())
    executed_timestamp = db.Column(db.DateTime, unique=False, nullable=True, default=None)

    action_type = db.relationship('ActionTypes', backref='actions', lazy='joined')
    user = db.relationship('Users', backref='actions', lazy='joined')

from optview import db
from models.base_mixin import BaseMixin

class ActionTypes(BaseMixin, db.Model):
    __tablename__ = "action_types"

    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(250), unique=True, nullable=False)
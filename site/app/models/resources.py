
from optview import db
from models.base_mixin import BaseMixin

class Resources(BaseMixin, db.Model):
    __tablename__ = "plan_resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    name_singular = db.Column(db.String(250), unique=True, nullable=False)

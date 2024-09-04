
from optview import db


class Resources(db.Model):
    __tablename__ = "plan_resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)


from optview import db


class Currencies(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    name_plural = db.Column(db.String(250), unique=True, nullable=False)

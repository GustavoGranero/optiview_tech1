
from optview import db
from models.base_mixin import BaseMixin


class Currencies(BaseMixin, db.Model):
    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    name_plural = db.Column(db.String(250), unique=True, nullable=False)

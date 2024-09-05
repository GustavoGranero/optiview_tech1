
from optview import db
from models.base_mixin import BaseMixin


class Periods(BaseMixin, db.Model):
    __tablename__ = "plan_periods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    period = db.Column(db.Interval, unique=True, nullable=False)
    name_plural = db.Column(db.String(250), unique=True, nullable=False)
    unit_name = db.Column(db.String(250), unique=True, nullable=False)
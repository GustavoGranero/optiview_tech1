
from optview import db


class Periods(db.Model):
    __tablename__ = "plan_periods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    period = db.Column(db.Interval, unique=True, nullable=False)

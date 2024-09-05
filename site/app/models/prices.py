from optview import db
from models.base_mixin import BaseMixin


class Prices(BaseMixin, db.Model):
    __tablename__ = "plan_prices"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(), unique=False, nullable=False, default=None)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), unique=False, nullable=False, default=None)
    period_id = db.Column(db.Integer, db.ForeignKey('plan_periods.id'), unique=False, nullable=False, default=None)

    currency = db.relationship('Currencies', backref='plan_prices', lazy='joined')
    period = db.relationship('Periods', backref='plan_prices', lazy='joined')

from optview import db
from models.base_mixin import BaseMixin


class Plans(BaseMixin, db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    price_id = db.Column(db.Integer, db.ForeignKey('plan_prices.id'), unique=False, nullable=False, default=None)

    price = db.relationship('Prices', backref='plans', lazy='joined')

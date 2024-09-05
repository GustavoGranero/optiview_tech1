from optview import db
from models.base_mixin import BaseMixin


class ResourceLimits(BaseMixin, db.Model):
    __tablename__ = "plan_resource_limits"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), unique=False, nullable=False, default=None)
    resource_id = db.Column(db.Integer, db.ForeignKey('plan_resources.id'), unique=False, nullable=False, default=None)
    limit = db.Column(db.Integer, unique=False, nullable=True, default=None)
    period_id = db.Column(db.Integer, db.ForeignKey('plan_periods.id'), unique=False, nullable=True, default=None)

    plan = db.relationship('Plans', backref='plan_resource_limits', lazy='joined')
    resource = db.relationship('Resources', backref='plan_resource_limits', lazy='joined')
    period = db.relationship('Periods', backref='plan_resource_limits', lazy='joined')
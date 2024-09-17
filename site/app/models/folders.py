import uuid

from optview import db
from models.base_mixin import BaseMixin

def uuid_default(context):
    return uuid.uuid4()

class Folders(BaseMixin, db.Model):
    __tablename__ = "folders"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Uuid, unique=True, nullable=False, default=uuid_default)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False, default=None)
    name = db.Column(db.String(250), unique=True, nullable=False)

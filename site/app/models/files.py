import uuid

from optview import db
from models.base_mixin import BaseMixin

def uuid_default(context):
    return uuid.uuid4()

class Files(BaseMixin, db.Model):
    __tablename__ = "folders"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Uuid, unique=True, nullable=False, default=uuid_default)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False, default=None)
    folder_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False, default=None)
    name = db.Column(db.String(250), unique=False, nullable=False)
    file = db.Column(db.LargeBinary, unique=False, nullable=False)

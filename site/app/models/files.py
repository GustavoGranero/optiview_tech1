import uuid
from math import floor
from math import log

from optview import db
from models.base_mixin import BaseMixin

def uuid_default(context):
    return uuid.uuid4()

class Files(BaseMixin, db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Uuid, unique=True, nullable=False, default=uuid_default)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False, default=None)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), unique=False, nullable=False, default=None)
    name = db.Column(db.String(250), unique=False, nullable=False)
    file = db.Column(db.LargeBinary, unique=False, nullable=False)

    user = db.relationship('Users', backref='files', lazy='joined')
    files_processed = db.relationship('FilesProcessed', backref='files', lazy='joined', cascade="all,delete")
    
    @property
    def file_size(self):
        size = len(self.file)
        power = 0 if size <= 0 else floor(log(size, 1024))
        return f"{round(size / 1024 ** power, 2)} {['B', 'KB', 'MB', 'GB', 'TB'][int(power)]}"
    
    
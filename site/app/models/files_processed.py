import uuid
from math import floor
from math import log

from optview import db
from models.base_mixin import BaseMixin

def uuid_default(context):
    return uuid.uuid4()

class FilesProcessed(BaseMixin, db.Model):
    __tablename__ = "files_processed"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Uuid, unique=True, nullable=False, default=uuid_default)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False, default=None)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), unique=False, nullable=False, default=None)
    parent_file_id = db.Column(db.Integer, db.ForeignKey('files.id'), unique=False, nullable=False, default=None)
    name = db.Column(db.String(250), unique=False, nullable=False)
    file = db.Column(db.LargeBinary, unique=False, nullable=False)
    processed_type_id = db.Column(db.Integer, db.ForeignKey('files_processed_types.id'), unique=False, nullable=False, default=None)

    user = db.relationship('Users', backref='files_processed', lazy='joined')
    processed_file_type = db.relationship('FilesProcessedTypes', backref='files_processed', lazy='joined')
    files_processed_results = db.relationship(
        'FilesProcessedResults', 
        backref='files_processed', 
        lazy='joined', 
        cascade="all,delete"
        )
    
    @property
    def file_size(self):
        size = len(self.file)
        power = 0 if size <= 0 else floor(log(size, 1024))
        return f"{round(size / 1024 ** power, 2)} {['B', 'KB', 'MB', 'GB', 'TB'][int(power)]}"
    
    
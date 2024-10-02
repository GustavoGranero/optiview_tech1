from optview import db
from models.base_mixin import BaseMixin

class FilesProcessedTypes(BaseMixin, db.Model):
    __tablename__ = "files_processed_types"

    id = db.Column(db.Integer, primary_key=True)
    file_processed_type = db.Column(db.String(250), unique=True, nullable=False)

from sqlalchemy.dialects.postgresql import JSON

from optview import db
from models.base_mixin import BaseMixin



class FilesProcessedResults(BaseMixin, db.Model):
    __tablename__ = "files_processed_results"

    id = db.Column(db.Integer, primary_key=True)
    plan_file_id = db.Column(db.Integer, db.ForeignKey('files_processed.id'), unique=False, nullable=False, default=None)
    code = db.Column(db.String(250), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    image_plan = db.Column(db.LargeBinary, unique=False, nullable=False)
    image_plan_box = db.Column(JSON, unique=False, nullable=False)
    image_table_line = db.Column(db.LargeBinary, unique=False, nullable=False)
    image_table_line_box = db.Column(JSON, unique=False, nullable=False)

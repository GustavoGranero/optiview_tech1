from optview import db


class HashTypes(db.Model):
    __tablename__ = "hash_types"

    id = db.Column(db.Integer, primary_key=True)
    hash_type = db.Column(db.String(250), unique=True, nullable=False)
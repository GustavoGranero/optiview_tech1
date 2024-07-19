from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL

def get_database_url(app):
        url_object = URL.create(
            "postgresql+psycopg2",
            username=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST'],
            database=app.config['DATABASE_NAME'],
            port=app.config['DATABASE_PORT'],
        )
        return url_object

def get_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url(app)
    db = SQLAlchemy(app)
    return db
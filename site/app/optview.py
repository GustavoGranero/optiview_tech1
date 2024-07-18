import datetime

from flask import Flask
from flask import session
from flask import render_template
# from flask import request
# from flask import url_for
# from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL
from flask_login import current_user
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

def get_database_url():
        url_object = URL.create(
            "postgresql+psycopg2",
            username=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST'],
            database=app.config['DATABASE_NAME'],
            port=app.config['DATABASE_PORT'],
        )
        return url_object

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")

app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
db = SQLAlchemy(app)


@app.route("/")
@app.route("/<name>")
def templates(name = "home.html"):
    session['authenticated'] = False

    if name in app.config['PAGES_NO_AUTHENTICAN_REQUIRED']:
        session.pop('redirect', None)
    elif not session['authenticated']:
        session['redirect'] = name
        name = 'login.html'

    if session['authenticated'] and 'redirect' in session:
        name = session['redirect']
        session.pop('redirect', None)
    
    return render_template(name)


    







    

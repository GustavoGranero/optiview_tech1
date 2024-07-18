import datetime

from flask import Flask
from flask import session
from flask import render_template
# from flask import request
# from flask import url_for
# from flask import redirect
from sqlalchemy import URL
from sqlalchemy import create_engine

def get_database_engine():
    url_object = URL.create(
        "postgresql",
        username=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASSWORD'],
        host=app.config['DATABASE_HOST'],
        database=app.config['DATABASE_NAME'],
    )

    engine = create_engine(url_object)
    return engine

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")
app.config.from_pyfile('config.py')
engine = get_database_engine()

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


    







    

import datetime

from flask import Flask
from flask import session
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")
app.config.from_pyfile('config.py')


def authentication_test():
    # verificar aqui se está autenticado ...
    #  ... se estiver vai para a página
    # ... se não estiver vai para o login
    # chamar isso em todas as páginas
    pass

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


    







    

from flask import (
    Flask,
    session,
    request,
    render_template,
    redirect,
    url_for,
)
from flask_login import (
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)


from database import get_database

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")
app.config.from_pyfile('config.py')
db = get_database(app)

from models.users import Users
from auth import get_authenticated_user
from auth import get_authenticated_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    user = Users.query.get(user_id)
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    user_name = request.form.get("email")
    password = request.form.get("senha")

    if (user := get_authenticated_user(user_name, password)) is not None:
        login_user(user)
        if 'redirect' in session:
            name = session['redirect']
            session.pop('redirect')
            return render_template(name)
        else:
            return render_template("home.html")

    return render_template("login.html")
 
 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("home.html")

@app.route("/")
@app.route("/<name>")
def templates(name = "home.html"):
    if name in app.config['PAGES_NO_AUTHENTICAN_REQUIRED']:
        session.pop('redirect', None)
    elif not current_user.is_authenticated:
        session['redirect'] = name
        name = 'login.html'

    if current_user.is_authenticated and 'redirect' in session:
        name = session['redirect']
        session.pop('redirect', None)
    
    return render_template(name)


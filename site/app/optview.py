import re

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
from sqlalchemy import exc

from database import get_database

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")
app.config.from_pyfile('config.py')
db = get_database(app)

from models.users import Users
from auth import get_authenticated_user
from auth import get_authenticated_user
from auth import get_hash

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/user", methods=["GET", "POST"])
def user():
    messages = []
    if current_user.is_authenticated:
        # TODO update user
        pass
    else:
        # create new user is only allowed if you are not logged in
        user_name = request.form.get("user")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        phone = request.form.get("phone")

        data_valid = True
        if password1 != password2:
            messages.append(f"A senha e a confirmação são diferentes.")
            data_valid = False
        else:
            password = password1

            if not (re.search(r"[a-zç]", password) is not None and 
                    re.search(r"[A-ZÇ]", password) is not None and 
                    (re.search(r"[0-9]", password) is not None or re.search(r"[!@#$%^&\*\(\)-_=+\[\]\{\}\/\|/\\\?\<\>.,~`]", password) is not None)):
                messages.append(f"A senha deve ter maiúsculas, minúsculas, e números ou símbolos.")
                data_valid = False

        if len(password)<8:
            messages.append(f"A senha deve ter ao menos 8 caracteres")
            data_valid = False
        if not (re.match(r'[\d -]', phone) and len(phone.replace(' ','').replace('-', '')) >= 6):
            messages.append(f"O telefone pode conter apenas espaços, números e - e tem de ter ao menos 6 dígitos.")
            data_valid = False
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messages.append(f"O e-mail é inválido")
            data_valid = False

        if data_valid:
            user_by_name = Users.query.filter_by(user_name = user_name).first()
            user_by_email= Users.query.filter_by(email = email).first()
            user_by_phone = Users.query.filter_by(phone = phone).first()

            if user_by_name is None and user_by_email is None and user_by_phone is None:

                try:
                    new_user = Users(user_name=user_name, email=email, phone=phone, hash=get_hash(user_name, password))
                    db.session.add(new_user)   
                    db.session.commit()

                    messages.append(f"Usuário criado, você receberá um e-mail e um SMS para confirmar e-mail e telefone.")
                    messages.append("Após confirmar estes dados poderá fazer login.")
                except exc.SQLAlchemyError as e:
                    # TODO log error
                    messages.append(f"Houve um erro na criação do usuário.")


            else:
                if user_by_name is not None:
                    messages.append(f"Este usuário já existe no cadastro utilize outro.")
                if user_by_email is not None:
                    messages.append(f"Este e-mail já existe no cadastro utilize outro.")
                if user_by_phone is not None:
                    messages.append(f"Este telefone já existe no cadastro utilize outro.")

    context = {
        'messages': messages,
        'user_name': user_name,
        'email': email,
        'password1': password1,
        'password2': password2,
        'phone': phone,
        'input_class': 'not-empty',
    }
    return render_template("cadastro.html", **context)

@login_manager.user_loader
def loader_user(user_id):
    user = Users.query.get(user_id)
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    messages = []
    user_name = request.form.get("user-or-email")
    password = request.form.get("password")

    try:
        if (user := get_authenticated_user(user_name, password)) is not None:
            login_user(user)
            if 'redirect' in session:
                name = session['redirect']
                session.pop('redirect')
                return render_template(name)
            else:
                return render_template("home.html")
        else:
            messages.append("Usuário ou senha inválidos. Tente novamente.")
    except Exception:
        messages.append("Houve um erro na validação do usuário e senha.")

    context = {
        'messages': messages,
    }
    return render_template("login.html", **context)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("home.html")

@app.route("/")
@app.route("/<name>")
def templates(name = "home.html"):
    if name in app.config['PAGES_NO_AUTHENTICANTION_REQUIRED']:
        session.pop('redirect', None)
    elif not current_user.is_authenticated:
        session['redirect'] = name
        name = 'login.html'

    if current_user.is_authenticated and 'redirect' in session:
        name = session['redirect']
        session.pop('redirect', None)
    
    return render_template(name)


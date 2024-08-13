import re

from flask import (
    Flask,
    session,
    request,
    render_template,
    redirect,
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
from models.plans import Plans
from models.hash_types import HashTypes
from models.action_types import ActionTypes
from models.actions import Actions
from auth import (
    get_authenticated_user,
    get_hash,
    is_suspended,
)
import email_send
from actions import execute_action

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/action/<token>", methods=["GET", "POST"])
def action(token):
    messages, resend_verification = execute_action(token)

    context = {
        'messages': messages,
        'resend_verification': resend_verification,
    }
    return render_template("login.html", **context)

@app.route("/user", methods=["GET", "POST"])
def user():
    messages = []
    if current_user.is_authenticated:
        # TODO update user
        pass
    else:
        # create new user is only allowed if you are not logged in
        user_name = request.form.get("user")
        full_name = request.form.get("full_name")
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
        if len(full_name)<1:
            messages.append(f"O nome completo não pode ser vazio")       

        if data_valid:
            user_by_name = Users.get_one(user_name = user_name)
            user_by_email= Users.get_one(email = email)
            user_by_phone = Users.get_one(phone = phone)

            if user_by_name is None and user_by_email is None and user_by_phone is None:

                try:
                    new_user = Users.add(user_name=user_name, full_name=full_name, email=email, phone=phone, hash=get_hash(user_name, password))

                    messages.append("Usuário criado, você receberá um e-mail para confirmar o e-mail e telefone.<br>Após confirmar estes dados poderá fazer login.")

                    ok, code, message = email_send.send_email_confirmation(app, new_user)
                    if not ok:
                        messages.append("Houve um erro no envio de seu e-mail. Tente fazer login mais tarde.")
                        # TODO log error code and message

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
        'full_name': full_name,
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
    resend_verification = False
    user_name = request.form.get("user-or-email")
    password = request.form.get("password")

    try:
        if is_suspended(user_name):
                Users.update_login_failure(user_name, failed=False)
                messages.append("Muitas tentativas de login sem sucesso.<br>Login temporariamente bloqueado.<br>Tente mais tarde ou altere sua senha.")
        else:
            if (user := get_authenticated_user(user_name, password)) is not None:
                if not user.verified:
                    resend_verification = True
                    messages.append("Você precisa ativar sua conta.<br>Verifique seu e-mail para ativar.")
                else:
                    Users.update_login_failure(user_name, failed=False)
                    login_user(user)
                    if 'redirect' in session:
                        name = session['redirect']
                        session.pop('redirect')
                        return redirect(f"/{name}")
                    else:
                        return redirect("/home.html")
            else:
                Users.update_login_failure(user_name, failed=True)
                messages.append("Usuário ou senha inválidos. Tente novamente.")
    except Exception as e:
        # TODO log the error
        messages.append("Houve um erro na validação do usuário e senha.")

    context = {
        'messages': messages,
        'resend_verification': resend_verification,
    }
    return render_template("login.html", **context)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    context = {
        'user': current_user,
    }
    return redirect("/home.html")

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
    
    context = {
        'user': current_user,
    }
    return render_template(name, **context)

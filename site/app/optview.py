import re
import os

from flask import (
    Flask,
    session,
    request,
    render_template,
    redirect,
    abort,
    Response,
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
from validate_fields import (
    is_valid_password,
    is_valid_password_length,
    normalize_phone,
    is_valid_phone,
    is_valid_email,
    is_valid_full_name,
    is_valid_user_name,
)
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
    return execute_action(token, request)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    messages = []
    user_or_email = request.form.get("user-or-email")

    user_by_name = Users.get_one(user_name = user_or_email)
    user_by_email= Users.get_one(email = user_or_email)
    
    if user_by_name is not None:
        user = user_by_name
    elif user_by_email is not None:
        user = user_by_email
    else:
        user = None

    if user is not None:

        try:
            ok, code, message = email_send.send_email_recorver_password(app, user)
            if ok:
                messages.append("Você receberá um e-mail com instruções para mudar a senha.")
            else:
                messages.append("Houve um erro no envio de seu e-mail. Faça o pedido novamente mais tarde.")
                # TODO log error code and message

        except exc.SQLAlchemyError as e:
            # TODO log error
            messages.append(f"Houve um erro no pedido de mudança de senha.")

    else:
        messages.append(f"Este usuário ou e-mail não foi encontrado.")

    context = {
        'messages': messages,
    }
    return render_template("request_password_reset.html", **context)

@app.route("/user", methods=["GET", "POST"])
def user():
    messages = []
    if current_user.is_authenticated:
        user_name = request.form.get("user")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        phone = request.form.get("phone")
        phone_normalized = normalize_phone(phone)


        data_valid = True
        if not is_valid_full_name(full_name):
            messages.append("O nome completo não pode ser vazio")
            data_valid = False
        if not is_valid_phone(phone):
            messages.append(f"O telefone pode conter apenas espaços, números e - e tem de ter ao menos 6 dígitos.")
            data_valid = False
        if user_name is not None:
            messages.append("O campo nome de usuário não pode ser alterado.")
            data_valid = False
        if email is not None:
            messages.append("O campo e-mail não pode ser alterado.")
            data_valid = False
        if password1 is not None or password2 is not None:
            messages.append("A senha não pode ser alterada.<br>Utilize o link abaixo para mudar a senha.")
            data_valid = False

        if data_valid:
            user_by_phone = Users.query.filter(Users.phone_normalized == phone_normalized, Users.id != current_user.id).first()

            if user_by_phone is None:

                try:
                    current_user.full_name = full_name
                    current_user.phone = phone
                    current_user.phone_normalized = phone_normalized
                    db.session.commit()

                    # TODO create send_changed_user_data and e-mail templates
                    # ok, code, message = email_send.send_changed_user_data(app, current_user)
                    # if not ok:
                    #     messages.append("Houve um erro no envio de seu e-mail.")
                    #     # TODO log error code and message

                    messages.append("Dados alterados.")

                except exc.SQLAlchemyError as e:
                    # TODO log error
                    messages.append("Houve um erro na alteração dos dados do usuário.")

            else:
                messages.append("Este telefone já existe no cadastro utilize outro.")


        context = {
            'messages': messages,
            'user': current_user,
            'input_class': 'not-empty',
        }
    else:
        # create new user is only allowed if you are not logged in
        user_name = request.form.get("user")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        phone = request.form.get("phone")
        phone_normalized = normalize_phone(phone)

        data_valid = True
        if password1 != password2:
            messages.append(f"A senha e a confirmação são diferentes.")
            data_valid = False
        else:
            password = password1

            if not is_valid_password(password):
                messages.append("A senha deve ter maiúsculas, minúsculas, e números ou símbolos.")
                data_valid = False

            if not is_valid_password_length(password):
                messages.append("A senha deve ter ao menos 8 caracteres")
                data_valid = False
                
        if not is_valid_phone(phone):
            messages.append(f"O telefone pode conter apenas espaços, números e - e tem de ter ao menos 6 dígitos.")
            data_valid = False
        if not is_valid_email(email):
            messages.append(f"O e-mail é inválido")
            data_valid = False
        if not is_valid_user_name(user_name):
            messages.append("O nome de usuário não pode ser vazio")
            data_valid = False
        if is_valid_email(user_name):
            # if other user can use an e-mail as a login ...
            # ... if this e-mail is used by another user ...
            # ... this e-mail could not be used to login or recover password
            messages.append("O nome de usuário não pode ser um e-mail")
            data_valid = False
        if not is_valid_full_name(full_name):
            messages.append("O nome completo não pode ser vazio")
            data_valid = False

        if data_valid:
            user_by_name = Users.get_one(user_name = user_name)
            user_by_email= Users.get_one(email = email)
            user_by_phone = Users.get_one(phone_normalized = phone_normalized)

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
                    messages.append("Houve um erro na criação do usuário.")

            else:
                if user_by_name is not None:
                    messages.append("Este usuário já existe no cadastro utilize outro.")
                if user_by_email is not None:
                    messages.append("Este e-mail já existe no cadastro utilize outro.")
                if user_by_phone is not None:
                    messages.append("Este telefone já existe no cadastro utilize outro.")

        context = {
            'messages': messages,
            'user': user,
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
    user_name_or_email = request.form.get("user-or-email")
    password = request.form.get("password")

    try:
        if is_suspended(user_name_or_email):
                Users.update_login_failure(user_name_or_email, failed=True)
                messages.append("Muitas tentativas de login sem sucesso.<br>Login temporariamente bloqueado.<br>Tente mais tarde ou altere sua senha.")
        else:
            if (user := get_authenticated_user(user_name_or_email, password)) is not None:
                if not user.verified:
                    resend_verification = True
                    messages.append("Você precisa ativar sua conta.<br>Verifique seu e-mail para ativar.")
                else:
                    Users.update_login_failure(user_name_or_email, failed=False)
                    login_user(user)
                    if 'redirect' in session:
                        name = session['redirect']
                        session.pop('redirect')
                        return redirect(f"/{name}")
                    else:
                        return redirect("/home.html")
            else:
                Users.update_login_failure(user_name_or_email, failed=True)
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
    
    filename = os.path.join(os.path.dirname(__file__), f'../web/{name}')
    if not os.path.isfile(filename):
        name = 'not_found.html'
    
    context = {
        'user': current_user,
    }
    return render_template(name, **context)

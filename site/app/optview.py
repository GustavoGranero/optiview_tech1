import re
import os
import io
import pathlib

from flask import (
    Flask,
    session,
    request,
    render_template,
    redirect,
    abort,
    Response,
    send_file,
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

# initalized before imports that use them
app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")
app.config.from_pyfile('config.py')
db = get_database(app)

from models.users import Users
from models.plans import Plans
from models.hash_types import HashTypes
from models.action_types import ActionTypes
from models.actions import Actions
from models.periods import Periods
from models.currencies import Currencies
from models.prices import Prices
from models.resources import Resources
from models.resource_limits import ResourceLimits
from models.folders import Folders
from models.files import Files
from models.files_processed import FilesProcessed
from models.files_processed_types import FilesProcessedTypes
from models.files_processed_results import FilesProcessedResults
from validate_fields import (
    is_valid_password,
    is_valid_password_length,
    normalize_phone,
    is_valid_phone,
    is_valid_email,
    is_valid_full_name,
    is_valid_user_name,
    is_valid_uuid,
)
from auth import (
    get_authenticated_user,
    get_hash,
    is_suspended,
)
import email_send
from folders import get_new_folder_name
from actions import execute_action
from process_files import (
    is_valid_file_type,
    extract_images_from_pdf,
    extract_tables_from_image,
    process_images,
)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/validate_file_for_process/<uuid>", methods=["GET", "POST"])
@app.route("/validate_file_for_process/image/<image_uuid>", methods=["GET", "POST"])
@login_required
def validate_file_for_process(uuid=None, image_uuid=None):
    status = 'Ok'
    message = ''

    if image_uuid is not None:
        uuid = image_uuid

    if not is_valid_uuid(uuid):
        status = 'Error'
        message = 'A UUID é inválida.'
    else:
        try:
            if image_uuid is not None:
                file = FilesProcessed.get_one(user_id=current_user.id, uuid=uuid)
            else:
                file = Files.get_one(user_id=current_user.id, uuid=uuid)
            if file is None:
                status = 'Error'
                message = 'O arquivo não existe no servidor.'
            elif pathlib.Path(file.name).suffix.lower() == '.dwg':
                status = 'Error'
                message = 'O processamento de arquivos do tipo DWG<br>ainda não foi implementado.'
        except exc.SQLAlchemyError as e:
            # TODO log error
            status = 'Error'
            message = 'Houve um erro no processamento do arquivo'

    status = {
        'status': status,
        'message': message
    }
    return status

@app.route("/file_process/<uuid>", methods=["GET", "POST"])
@login_required
def file_process(uuid):
    status = 'Ok'
    message = ''
    images = []

    if not is_valid_uuid(uuid):
        abort(400, {'error': 'UUID inválida.'})

    try:
        file = Files.get_one(user_id=current_user.id, uuid=uuid)
        if file is None:
            abort(404)
        elif pathlib.Path(file.name).suffix.lower() == '.dwg':
            status = 'Error'
            message = 'O processamento de arquivos do tipo DWG<br>ainda não foi implementado.'
        else:
            status, message = extract_images_from_pdf(app, current_user, uuid)

            if status == "Ok":
                status, message = extract_tables_from_image(app, current_user, uuid)

            # prepare data of images created by the processing to be returned to add on the page
            if status == "Ok":
                # TODO maybe use Files.get_one(user_id=current_user.id, uuid=uuid) again to refrese FilesProcessed
                files_processed = FilesProcessed.query
                files_processed = files_processed.filter_by(user_id=current_user.id, parent_file_id=file.id)
                files_processed = files_processed.order_by(FilesProcessed.processed_type_id, FilesProcessed.id)

                process_images(app, files_processed)

                for file_processed in files_processed:
                    image = { 
                        'uuid': str(file_processed.uuid),
                        'name': file_processed.name,
                        'size': file_processed.file_size,
                        'type': file_processed.processed_file_type.file_processed_type,
                    }
                    images.append(image)
                    
    except exc.SQLAlchemyError as e:
        # TODO log error
        status = 'Error'
        message = 'Houve um erro no processamento do arquivo'
    
    
    status = {
        'status': status,
        'message': message,
        'images': images,
    }
    return status

@app.route("/image/<uuid>", methods=["GET", "POST"])
@login_required
def image(uuid):
    if is_valid_uuid(uuid):
        file = FilesProcessed.get_one(user_id=current_user.id, uuid=uuid)
        
    if not is_valid_uuid(uuid):
        abort(401)
    elif file is None:
        abort(404)
    else:
        return send_file(
            io.BytesIO(file.file),
            as_attachment=False,
            mimetype='image/png'
        )

@app.route("/files_processed/<uuid>", methods=["GET", "POST"])
@app.route("/files_processed/image/<image_uuid>", methods=["GET", "POST"])
@login_required
def files_processed(uuid=None, image_uuid=None):
    status = 'Ok'
    message = ''
    file_name = ''
    images = []

    file_processed = None
    file = None

    if uuid is None and image_uuid is not None:
        # images was passed: get uuid of parent file 
        if is_valid_uuid(image_uuid):
            file_processed = FilesProcessed.get_one(user_id=current_user.id, uuid=image_uuid)

        if not is_valid_uuid(image_uuid):
            status = 'Error'
            message = f"A UUID da imagem é inválida."
        elif file_processed is None:
            status = 'Error'
            message = f"A imagem com UUID '{image_uuid}' não existe."
        else:
            file = Files.get_one(user_id=current_user.id, id=file_processed.parent_file_id)
            uuid = file.uuid

    if status == "Ok":
        status, message = extract_images_from_pdf(app, current_user, uuid)

    if status == "Ok":
        if file is None:
            file = Files.get_one(user_id=current_user.id, uuid=uuid)

        file_name = file.name
        for index, file_processed in enumerate(file.files_processed):
            image = { 
                'index': index,
                'name': file_processed.name,
                'uuid': str(file_processed.uuid),
                'type_name': file_processed.processed_file_type.name,
                'owner': file_processed.user.user_name,
                'size' : file_processed.file_size,
            }
            images.append(image)

    context = {
        'status': status,
        'message': message,
        'user': current_user,
        'file_name': file_name,
        'images': images,
        'image_uuid': image_uuid,
    }
    return render_template('/files_processed.html', **context)

@app.route("/folder/<uuid>", methods=["GET", "POST"])
@login_required
def folder(uuid):
    status = 'Ok'
    message = ''

    if is_valid_uuid(uuid):
        folder = Folders.get_one(user_id=current_user.id, uuid=uuid)
        if folder is None:
            status = 'Error'
            message = 'Projeto não encontrado no servidor.'
    else:
        status = 'Error'
        message = 'UUID inválida.'
        folder = None

    context = {
        'status': status,
        'message': message,
        'user': current_user,
        'folder': folder,
    }
    return render_template("/folder.html", **context)

@app.route("/create_folder/", methods=["GET", "POST"])
@login_required
def create_folder():
    status = 'Ok'
    message = ''
    name = None
    uuid = None
    plan = current_user.plan
    resource_id = Resources.get_one(name='Projetos').id
    folders_limit = ResourceLimits.get_one(plan_id=plan.id, resource_id=resource_id).limit
    folders_count = len(current_user.folders)
    if folders_count < folders_limit:
        try:
            new_folder_name = get_new_folder_name(app, current_user)
            new_folder = Folders.add(name=new_folder_name, user_id=current_user.id)
            name = new_folder.name,
            uuid = new_folder.uuid
        except  exc.SQLAlchemyError as e:
            # TODO log error
            status = 'Error'
            message = "Houve um erro na criação do novo folder."
    else:
        status = 'Error'
        message = f"O número máximo de projetos para o <br>plano {plan.name} foi atingido"
    
    status = {
        'status': status,
        'message': message,
        'name': name,
        'uuid': uuid,
    }
    return status

@app.route("/rename_folder/", methods=["GET", "POST"])
@login_required
def rename_folder():
    name = request.args.get("name")
    uuid = request.args.get("uuid")
    status = 'Ok'
    message = ''
    try:
        folder_alredy_exists = Folders.get_one(user_id = current_user.id, name = name)
        current_folder = Folders.get_one(user_id = current_user.id, uuid = uuid)
        if folder_alredy_exists is None and current_folder is not None:
            current_folder.name = name
            db.session.commit()
        elif current_folder is None:
            status = 'Error'
            message = f"O folder '{name}' não foi econtrado nor servidor."
            name = ''
        elif current_folder != folder_alredy_exists:
            # if current_folder and folder_alredy_exists are equal the name was not changed
            status = 'Error'
            message = f"O folder '{name}' já existe."
            name = current_folder.name
    except  exc.SQLAlchemyError as e:
        # TODO log error
        status = 'Error'
        message = "Houve um erro na renomeação do folder."
    
    status = {
        'status': status,
        'message': message,
        'name': name,
        'uuid': uuid,
    }
    return status

@app.route("/file/<uuid>", methods=["GET", "POST"])
@login_required
def download_file(uuid):
    if not is_valid_uuid(uuid):
        abort(400, {'error': 'UUID inválida.'})
    
    try:
        file = Files.get_one(user_id = current_user.id, uuid = uuid)
        if file is None:
            abort(404)

        return send_file(
            io.BytesIO(file.file),
            download_name=file.name,
            as_attachment=True
        )
    except exc.SQLAlchemyError as e:
        # TODO log error
        abort(500)

@app.route("/create_file/", methods=["GET", "POST"])
@login_required
def create_file():
    status = 'Ok'
    message = ''
    file_name = None
    uuid = ''
    file_owner = None
    file_size = None

    file_by_name = None
    folder_by_uuid = None
    file_data = None

    folder_uuid = request.form.get('folder_uuid')
    file = request.files.get('file')

    if file is not None:
        file_name = file.filename
        file_data = file.read()

    if is_valid_uuid(folder_uuid):
        folder_by_uuid = Folders.get_one(user_id = current_user.id, uuid = folder_uuid)
        file_by_name = Files.get_one(user_id=current_user.id, folder_id=folder_by_uuid.id, name=file_name)

    if not is_valid_uuid(folder_uuid):
        status = 'Error'
        message = f"A UUID da pasta é inválida."
    elif not is_valid_file_type(file_data, file_name):
        status = 'Error'
        message = f"O arquivo não é um dos tipos aceitos:<br>PDF ou DWG."
    elif file_by_name is not None:
        status = 'Error'
        message = f"O arquivo <br>'{file_name}'<br> já existe."
    elif folder_by_uuid is None:
        status = 'Error'
        message = f"O folder com UUID <br>'{folder_by_uuid}'<br> não existe no servidor."
    else:
        try:
            new_file = Files.add(user_id=current_user.id, folder_id=folder_by_uuid.id, name=file_name, file=file_data)
            uuid = new_file.uuid
            file_owner = new_file.user.user_name
            file_size = new_file.file_size
        except  exc.SQLAlchemyError as e:
            # TODO log error
            status = 'Error'
            message = "Houve um erro na criação do novo arquivo."

    status = {
        'status': status,
        'message': message,
        'name': file_name,
        'uuid': uuid,
        'owner': file_owner,
        'size' : file_size,
    }
    return status

@app.route("/delete_file//<uuid>", methods=["GET", "POST"])
@login_required
def delete_file(uuid):
    if not is_valid_uuid(uuid):
        abort(400, {'error': 'UUID inválida.'})
    
    try:
        file = Files.get_one(user_id = current_user.id, uuid = uuid)
        if file is None:
            abort(404)

        db.session.delete(file)
        db.session.commit()
        return {}
    except exc.SQLAlchemyError as e:
        # TODO log error
        abort(500)

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
            user_by_phone = Users.get_one(phone_normalized = phone_normalized)

            if user_by_phone.id == current_user.id:

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

@app.route("/plan_myplantai.html", methods=["GET", "POST"])
def plans():
    # filename = os.path.join(os.path.dirname(__file__), f'../web/{name}')
    plans = Plans.query.order_by(Plans.id).all()
    periods = Periods.query.order_by(Periods.id).all()
    
    context = {
        'periods': periods,
        'plans': plans,
    }
    return render_template('plan_myplantai.html', **context)

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

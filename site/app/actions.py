import re
from datetime import(
    datetime,
    timezone,
)

from flask import render_template

from optview import app, db
from auth import update_password
from models.actions import Actions

def execute_action(token, request=None):
    action = Actions.get_one(token=token)

    action_elapsed_time = datetime.now(timezone.utc) -  action.timestamp
    action_expired = action_elapsed_time.total_seconds() / 3600 >= app.config['EMAIL_REQUEST_EXPIRATION_TIME']
    action_executed = action.executed_timestamp is not None

    action_type = action.action_type.action_type
    if action_type == 'confirm_email':
        return execute_confirm_email(action, action_executed, action_expired)
    elif action_type == 'confirm_password_reset':
        return execute_confirm_password_reset(action, action_executed, action_expired, request)
    elif action_type == 'confirm_email_change_original':
        # TODO do action
        pass
    elif action_type == 'confirm_email_change_new':
        # TODO do action
        pass

    return 'Ação "{action_type}" não reconhecida.', False

def execute_confirm_email(action, action_executed, action_expired):
        if action_executed:
            messages = ['Esse pedido de ativação de conta já foi executado. Faça login.']
            resend_verification = False
        elif action_expired:
            messages = ['Esse pedido de ativacão de conta já expirou. Solicite outro.']
            resend_verification = True
        else:
            user = action.user
            user.verified = True
            action.executed_timestamp = datetime.now(timezone.utc)
            db.session.commit()
            
            messages = ['Seu e-mail foi verificado e sua conta ativada. Faça o login.']
            resend_verification = False

        context = {
            'messages': messages,
            'resend_verification': resend_verification,
        }           
        return render_template("login.html", **context)

def execute_confirm_password_reset(action, action_executed, action_expired, request):
    messages = []
    token = None
    resend_verification = None
    if action_executed:
        messages.append("Esse pedido de recuperação de senha já foi executado. Faça login.")
        resend_verification = False
        token = None
        page = "login.html"
    elif action_expired:
        messages.append("Esse pedido de recuperação de senha já expirou. Solicite outro.")
        resend_verification = True
        token = None
        page = "login.html"
    else:
        token = action.token
        resend_verification = None
        if len(request.form) == 0:
            # no post data received so it came from the confirmation e-mail: present change password page
            page = "change_password.html"
        else:
            # post data received so it came from change password page: change password and present login page
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            data_valid = True
            if password1 != password2:
                messages.append("A senha e a confirmação são diferentes.")
                data_valid = False
            else:
                password = password1

                if not (re.search(r"[a-zç]", password) is not None and 
                        re.search(r"[A-ZÇ]", password) is not None and 
                        (re.search(r"[0-9]", password) is not None or re.search(r"[!@#$%^&\*\(\)-_=+\[\]\{\}\/\|/\\\?\<\>.,~`]", password) is not None)):
                    messages.append("A senha deve ter maiúsculas, minúsculas, e números ou símbolos.")
                    data_valid = False

                if len(password)<8:
                    messages.append("A senha deve ter ao menos 8 caracteres")
                    data_valid = False

            if data_valid:
                update_password(action.user, password)
                user = action.user
                user.update_login_failure(user.user_name, failed=False)
                action.executed_timestamp = datetime.now(timezone.utc)
                db.session.commit()

                messages = ['Senha alterada. Faça login.']
                resend_verification = False
                token = None
                page = "login.html"
            else:
                page = "change_password.html"


    context = {
        'messages': messages,
        'resend_verification': resend_verification,
        'token': token
    }           
    return render_template(page, **context)
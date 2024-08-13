from datetime import(
    datetime,
    timezone,
)

from optview import app, db
from models.actions import Actions

def execute_action(token):
    action = Actions.get_one(token=token)

    action_elapsed_time = datetime.now(timezone.utc) -  action.timestamp
    action_expired = action_elapsed_time.total_seconds() / 3600 >= app.config['EMAIL_REQUEST_EXPIRATION_TIME']
    action_executed = action.executed_timestamp is not None

    action_type = action.action_type.action_type
    if action_type == 'confirm_email':
        return execute_confirm_email(action, action_executed, action_expired)
    elif action_type == 'confirm_password_reset':
        # TODO do action
        pass
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
            # user = action.user
            # user.verified = True
            # action.executed_timestamp = datetime.now(timezone.utc)
            # db.session.commit()
            
            messages = ['Seu e-mail foi verificado e sua conta ativada. Faça o login.']
            resend_verification = False

        return messages, resend_verification
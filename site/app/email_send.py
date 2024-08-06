import os

from mailersend import emails
from flask import render_template_string

def get_template(template_name):
    
    filename = os.path.join(os.path.dirname(__file__), f'../email_templates/{template_name}')
    with open(filename) as file:
        template = file.read()
    
    return template

def get_action_url(app, user):
    # TODO criar o modelo das tabelas action e action_types
    # TODO create action token
    token = '7799404457b3c2914DB395ea19ce0641'
    # TODO create token entry on action table
    # TODO create action URL
    url = app.config['EMAIL_ACTION_URL'].format(token=token)
    return url

def send_email_confirmation(app, user):
    template_name = app.config['EMAIL_TEMPLATE_CONFIRM_EMAIL']
    template = get_template(template_name)
    subject_template_name = app.config['EMAIL_TEMPLATE_CONFIRM_EMAIL_SUBJECT']
    subject_template = get_template(subject_template_name)

    variables = {
        'company': app.config['COMPANY'],
        'name': user.full_name,
        'product': app.config['PRODUCT'],
        'expiration_time': app.config['EMAIL_REQUEST_EXPIRATION_TIME'],
        'action_url': get_action_url(app, user),
        'login_url': app.config['EMAIL_LOGIN_URL'],
        'username':  user.user_name,
        'site_url': app.config['EMAIL_SITE_URL'],
    }

    subject =  render_template_string(subject_template, **variables)
    email_content = render_template_string(template, **variables)

    result = send_mail(app, subject, email_content, user)
    return result

def send_mail(app, subject, email_content, user):
    mailer = emails.NewEmail(app.config['EMAIL_API_TOKEN'])

    mail_body = {}

    mail_from = {
        "name": app.config['EMAIL_NAME_FROM'],
        "email": app.config['EMAIL_ADDRESS_FROM'],
    }

    recipients = [
        {
            "name": user.full_name,
            "email": user.email,
        }
    ]

    reply_to = {
        "name": app.config['EMAIL_NAME_FROM'],
        "email": app.config['EMAIL_ADDRESS_FROM'],
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(email_content, mail_body)
    # mailer.set_plaintext_content("This is the text content", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    result = mailer.send(mail_body)
    result_parts = result.split('\n')
    code = int(result_parts[0])
    message = result_parts[1]

    if 200 <= code < 300:
        ok = True
    else:
        ok = False

    return ok, code, message


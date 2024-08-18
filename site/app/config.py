from our_secrets import *

COMPANY = "Optiview Tech"
PRODUCT = "MyPlanAI"
LANGUAGE = "pt"

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = 'optview'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = SECRET_DATABASE_PASSWORD

SECRET_KEY = SECRET_SESSION_KEY

LOGIN_FAILED_ATTEMPTS_LIMIT = 3
LOGIN_SUSPENSION_TIME = 24

PAGES_NO_AUTHENTICANTION_REQUIRED = [
    'home.html', 
    'about.html', 
    'declaracao_estrategica.html', 
    'login.html', 
    'contact.html',
    'cadastro.html',
    'request_password_reset.html'
    ]

EMAIL_API_TOKEN = SECRET_EMAIL_API_TOKEN
EMAIL_ADDRESS_FROM = 'noreply@trial-7dnvo4drnzng5r86.mlsender.net'
EMAIL_NAME_FROM = 'OptiView Tech'

EMAIL_TEMPLATE_CONFIRM_EMAIL = f'confirm_email_{LANGUAGE}.html'
EMAIL_TEMPLATE_CONFIRM_EMAIL_CHANGE_ORIGINAL = f'confirm_email_change_original_{LANGUAGE}.html'
EMAIL_TEMPLATE_CONFIRM_EMAIL_CHANGE_NEW = f'confirm_email_change_new_{LANGUAGE}.html'
EMAIL_TEMPLATE_RECOVER_PASSWORD = f'recover_password_{LANGUAGE}.html'
EMAIL_TEMPLATE_CHANGED_PASSWORD = f'changed_password_{LANGUAGE}.html'
EMAIL_TEMPLATE_CHANGED_EMAIL = f'changed_email_{LANGUAGE}.html'

EMAIL_TEMPLATE_CONFIRM_EMAIL_SUBJECT = f'confirm_email_subject_{LANGUAGE}.txt'
EMAIL_TEMPLATE_CONFIRM_EMAIL_CHANGE_ORIGINAL_SUBJECT = f'confirm_email_change_original_subject_{LANGUAGE}.txt'
EMAIL_TEMPLATE_CONFIRM_EMAIL_CHANGE_NEW_SUBJECT = f'confirm_email_change_new_subject_{LANGUAGE}.txt'
EMAIL_TEMPLATE_RECOVER_PASSWORD_SUBJECT = f'recover_password_subject_{LANGUAGE}.txt'
EMAIL_TEMPLATE_CHANGED_PASSWORD_SUBJECT = f'changed_password_subject_{LANGUAGE}.txt'
EMAIL_TEMPLATE_CHANGED_EMAIL_SUBJECT = f'changed_email_subject_{LANGUAGE}.txt '

EMAIL_REQUEST_EXPIRATION_TIME = 24
EMAIL_SITE_URL = 'http://127.0.0.1:5000' # temporário para teste
EMAIL_LOGIN_URL = f'{EMAIL_SITE_URL}/login.html'
EMAIL_REQUEST_PASSWORD_CHANGE_URL = f'{EMAIL_SITE_URL}/request_password_reset.html'
EMAIL_ACTION_URL = f'{EMAIL_SITE_URL}/action/{{token}}'
EMAIL_LOGO_URL = f'{EMAIL_SITE_URL}/images/logo_black.png'

ACTION_TYPE_CONFIRM_EMAIL = 'confirm_email'
ACTION_TYPE_CONFIRM_PASSWORD_RESET = 'confirm_password_reset'
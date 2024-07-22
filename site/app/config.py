from our_secrets import *

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "optview"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = SECRET_DATABASE_PASSWORD

SECRET_KEY = SECRET_SESSION_KEY

PAGES_NO_AUTHENTICAN_REQUIRED = [
    'home.html', 
    'about.html', 
    'declaracao_estrategica.html', 
    'login.com', 
    'contact.html',
    'cadastro.html',
    ]

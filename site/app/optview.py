from flask import Flask
from flask import render_template
import datetime

app = Flask(__name__, static_url_path='',  static_folder='../web',)

def authentication_test():
        # verificar aqui se está autenticado ...
    #  ... se estiver vai para a página
    # ... se não estiver vai para o login
    # chamar isso em todas as páginas
    pass

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
    print("aaaaa")
    return render_template("hello_there.html", name=name, date=datetime.datetime.now())

# @app.route("/login.html")
# def login():
#     return app.send_static_file("login.html")


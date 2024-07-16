from flask import Flask
from flask import render_template
import datetime

app = Flask(__name__, static_url_path='',  static_folder='../web', template_folder="../web")

def authentication_test():
    # verificar aqui se está autenticado ...
    #  ... se estiver vai para a página
    # ... se não estiver vai para o login
    # chamar isso em todas as páginas
    pass

@app.route("/")
@app.route("/<name>")
def templates(name = "home.html"):
    return render_template(name)


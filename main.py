import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
# Criar a instância do Flask
app = Flask(__name__)

# Habilitar CORS para permitir requisições de qualquer origem
CORS(app)

# Configurar pasta de upload e extensões permitidas
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Verifica se o post contém o arquivo
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Verifica se o arquivo tem um nome válido
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Verifica se o arquivo é permitido
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'filename': filename}), 200
    else:
        return jsonify({'error': 'File not allowed. Only JPEG or PNG files are accepted.'}), 400

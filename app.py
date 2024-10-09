import os
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from werkzeug.utils import secure_filename



# Carrega as credenciais do Firebase a partir da variável de ambiente
cred_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')

# Converte o JSON em um dicionário
cred_dict = json.loads(cred_json)

# Inicializa o Firebase
cred = credentials.Certificate('cred_dict')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'detec-serpentes.appspot.com'  
})

api = Flask(__name__)

# Extensões de arquivo permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload de uma foto
@api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowedFile(file.filename):
        return jsonify({'error': 'Extesao de arquivo nao permitido'}), 400
    
    # Segurança no nome do arquivo
    filename = secure_filename(file.filename)
    
    # Upload para o Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(f'imagesUsers/{filename}')
    blob.upload_from_file(file)  # Faz o upload do arquivo para o Firebase
    blob.make_public()
    
    return jsonify({'success': f'Arquivo {filename} foi recebido'}), 200

if __name__ == "__main__":
    api.run(debug=True)


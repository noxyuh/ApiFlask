import os
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from werkzeug.utils import secure_filename

# Carrega as credenciais do Firebase a partir da variável de ambiente
cred_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')

if cred_json:
    
    cred_dict = json.loads(cred_json)
    
    
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'detec-serpentes.appspot.com'  
    })
else:
    raise Exception('GOOGLE_APPLICATION_CREDENTIALS_JSON não foi encontrada nas variáveis de ambiente')

api = Flask(__name__)


ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowedFile(file.filename):
        return jsonify({'error': 'Extensão de arquivo não permitida'}), 400
    
    filename = secure_filename(file.filename)
    
    
    bucket = storage.bucket()
    blob = bucket.blob(f'imagesUsers/{filename}')
    blob.upload_from_file(file)  

    
    return jsonify({'success': f'Arquivo {filename} foi recebido', 'url': blob.public_url}), 200

if __name__ == "__main__":
    api.run(debug=True)


from flask import Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pandas as pd

bp = Blueprint('files', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../../output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Invalid file type. Please upload Excel file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        df = pd.read_excel(file_path)
        data = df.to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'data': data, 
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/list/<folder>', methods=['GET'])
def list_files(folder):
    try:
        if folder not in ['uploads', 'output']:
            return jsonify({'error': 'Invalid folder'}), 400
            
        folder_path = UPLOAD_FOLDER if folder == 'uploads' else OUTPUT_FOLDER
        files = []
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_stats = os.stat(file_path)
                files.append({
                    'name': filename,
                    'size': file_stats.st_size,
                    'modified': file_stats.st_mtime
                })
                
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/download/<folder>/<filename>', methods=['GET'])
def download_folder_file(folder, filename):
    try:
        if folder not in ['uploads', 'output']:
            return jsonify({'error': 'Invalid folder'}), 400
            
        folder_path = UPLOAD_FOLDER if folder == 'uploads' else OUTPUT_FOLDER
        file_path = os.path.join(folder_path, secure_filename(filename))
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
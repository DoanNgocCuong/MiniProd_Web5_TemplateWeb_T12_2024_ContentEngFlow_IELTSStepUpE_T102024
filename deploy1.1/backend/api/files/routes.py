from flask import Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pandas as pd
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('files', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../../output')
EXAMPLE_FOLDER = os.path.join(os.path.dirname(__file__), '../../example')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(EXAMPLE_FOLDER, exist_ok=True)

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
        if folder not in ['uploads', 'output', 'example']:
            return jsonify({'error': 'Invalid folder'}), 400
            
        folder_path = UPLOAD_FOLDER if folder == 'uploads' else (
            OUTPUT_FOLDER if folder == 'output' else EXAMPLE_FOLDER
        )
        items = []
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            logger.error(f'Folder not found: {folder_path}')
            return jsonify({'error': 'Folder not found'}), 404
        
        for item_name in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item_name)
            stats = os.stat(item_path)
            
            item_info = {
                'name': item_name,
                'size': stats.st_size,
                'modified': stats.st_mtime,
                'type': 'directory' if os.path.isdir(item_path) else 'file'
            }
            
            # Add extension info for files
            if os.path.isfile(item_path):
                item_info['extension'] = os.path.splitext(item_name)[1].lower()
            
            items.append(item_info)
                
        return jsonify({
            'success': True,
            'files': items
        })
        
    except Exception as e:
        logger.error(f'Error listing files in {folder}: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/download/<folder>/<path:filename>', methods=['GET'])
def download_folder_file(folder, filename):
    try:
        if folder not in ['uploads', 'output', 'example']:
            return jsonify({'error': 'Invalid folder'}), 400
            
        folder_path = UPLOAD_FOLDER if folder == 'uploads' else (
            OUTPUT_FOLDER if folder == 'output' else EXAMPLE_FOLDER
        )
        item_path = os.path.join(folder_path, secure_filename(filename))
        
        if not os.path.exists(item_path):
            return jsonify({'error': 'File or folder not found'}), 404
            
        # If it's a file, send it directly
        if os.path.isfile(item_path):
            return send_file(item_path, as_attachment=True)
            
        # If it's a directory, create a zip file
        if os.path.isdir(item_path):
            import tempfile
            import zipfile
            
            # Create temporary zip file
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            
            with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, item_path)
                        zipf.write(file_path, arc_name)
            
            return send_file(
                temp_zip.name,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f"{os.path.basename(item_path)}.zip"
            )
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/download/<folder>/all', methods=['GET'])
def download_all(folder):
    try:
        if folder not in ['uploads', 'output', 'example']:
            return jsonify({'error': 'Invalid folder'}), 400
            
        folder_path = UPLOAD_FOLDER if folder == 'uploads' else OUTPUT_FOLDER
        
        # Create temporary zip file
        import tempfile
        import zipfile
        
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arc_name)
        
        return send_file(
            temp_zip.name,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{folder}_all.zip"
        )
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
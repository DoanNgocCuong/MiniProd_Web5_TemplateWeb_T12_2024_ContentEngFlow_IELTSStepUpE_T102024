from flask import Flask, request, jsonify, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
import subprocess
from flask_cors import CORS
from api.scripts import bp as scripts_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(scripts_bp, url_prefix='/api/scripts')
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
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
        
        # Đọc file Excel và chuyển đổi thành JSON để gửi về frontend
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

@app.route('/update', methods=['POST'])
def update_file():
    data = request.json['data']
    filename = request.json['filename']

    # Chuyển đổi dữ liệu từ JSON sang DataFrame
    df = pd.DataFrame(data)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    df.to_excel(output_path, index=False)
    
    return jsonify({'message': 'File updated successfully', 'filename': filename})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

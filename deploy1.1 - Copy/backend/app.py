from flask import Flask
from flask_cors import CORS
from api.scripts import bp as scripts_bp
from api.files import bp as files_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(scripts_bp, url_prefix='/api/scripts')
app.register_blueprint(files_bp, url_prefix='/api/files')

if __name__ == '__main__':
    app.run(debug=True)

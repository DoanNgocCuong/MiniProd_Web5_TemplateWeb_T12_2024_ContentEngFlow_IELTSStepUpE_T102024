from flask import Flask, request
from flask_cors import CORS
from api.scripts import bp as scripts_bp
from api.files import bp as files_bp

app = Flask(__name__)
# CORS(app)  # cấp quyền cho tất cả các nguồn
# CORS(app, supports_credentials=True)  # Thêm supports_credentials nếu cần thiết

# # Cấu hình CORS đơn giản hơn
# CORS(app, resources={
#     r"/*": {
#         "origins": ["http://localhost:25038", "http://localhost:3000", "http://103.253.20.13:25038"],  # Chỉ cho phép các domain này
#         "methods": ["GET", "POST"],  # Chỉ các phương thức này được phép
#         "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],  # Chỉ định các headers cần thiết
#         "expose_headers": ["Authorization"],  # Các headers mà client có thể nhìn thấy
#         "supports_credentials": True  # Cho phép gửi cookie
#     }
# })

# @app.after_request
# def after_request(response):
#     # Lấy origin từ request
#     origin = request.headers.get('Origin')
#     allowed_origins = [
#         "http://localhost:25038",
#         "http://localhost:3000",
#         "http://103.253.20.13:25038"
#     ]
    
#     if origin in allowed_origins:
#         response.headers.add('Access-Control-Allow-Origin', origin)
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    
#     return response


# Cấu hình CORS đơn giản hơn
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:25038",
            "http://localhost:3000",
            "http://103.253.20.13:25038"
        ],
        "methods": ["GET", "POST"],  # Chỉ các methods cần thiết
        "allow_headers": ["Content-Type"]  # Headers cơ bản
    }
})

# Register blueprints
app.register_blueprint(scripts_bp, url_prefix='/api/scripts')
app.register_blueprint(files_bp, url_prefix='/api/files')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Tải biến môi trường từ .env
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Cấu hình từ .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Cấu hình CORS nếu cần (Quan trọng khi kết nối với Frontend)
    # Ví dụ đơn giản (Cần cài đặt flask-cors: pip install flask-cors)
    # from flask_cors import CORS
    # CORS(app) 
    
    # Khởi tạo các tiện ích
    db.init_app(app)
    bcrypt.init_app(app)

    # Đăng ký Blueprints (Routes/Controllers)
    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.customer_routes import customer_bp # <-- Đã thêm

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(customer_bp, url_prefix='/api/customers') # <-- Đã thêm

    return app

if __name__ == '__main__':
    app = create_app()
    # Tạo bảng CSDL khi khởi động (chỉ dùng cho phát triển/kiểm thử)
    with app.app_context():
        # Lệnh này sẽ tạo các bảng nếu chúng chưa tồn tại
        db.create_all() 
    
    app.run(debug=True)
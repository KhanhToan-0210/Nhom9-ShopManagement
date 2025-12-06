from flask import Blueprint, request, jsonify
from app import db, bcrypt
from models.user import User # Giả định đã tạo models/user.py
from utils.jwt_auth import generate_jwt, token_required
import requests
import os

auth_bp = Blueprint('auth_bp', __name__)

# POST /api/auth/login (Login thường)
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Thiếu Username hoặc Password'}), 400

    user = User.query.filter_by(username=username).first()

    # Kiểm tra user và mật khẩu (bcrypt)
    if user and user.password_hash and bcrypt.check_password_hash(user.password_hash, password):
        # Tạo JWT Token của hệ thống
        token = generate_jwt(user.id, user.role)
        return jsonify({'message': 'Đăng nhập thành công', 'token': token, 'role': user.role}), 200
    
    return jsonify({'message': 'Username hoặc Password không đúng'}), 401

# POST /api/auth/google (Login OAuth2) - Cần logic xử lý token
@auth_bp.route('/google', methods=['POST'])
def login_google():
    data = request.get_json()
    id_token = data.get('id_token')
    
    if not id_token:
        return jsonify({'message': 'Thiếu id_token của Google'}), 400
    
    # 1. Gửi token đến Google để xác thực
    GOOGLE_VERIFY_URL = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    response = requests.get(GOOGLE_VERIFY_URL)
    
    if response.status_code != 200:
        return jsonify({'message': 'Token Google không hợp lệ'}), 401
    
    google_data = response.json()
    google_id = google_data.get('sub') # ID duy nhất của user Google
    email = google_data.get('email')
    
    # 2. Tìm hoặc tạo user trong CSDL
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        # Nếu chưa có, tạo user mới
        user = User(
            username=email.split('@')[0], # Lấy phần trước @ làm username
            email=email,
            google_id=google_id,
            role='STAFF' # Mặc định là STAFF
        )
        db.session.add(user)
        db.session.commit()

    # 3. Tạo JWT Token của hệ thống và trả về
    token = generate_jwt(user.id, user.role)
    return jsonify({'message': 'Đăng nhập Google thành công', 'token': token, 'role': user.role}), 200

# GET /api/auth/me (Lấy thông tin user)
@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    user_id = request.current_user['sub']
    # Tìm user trong DB (trừ password_hash)
    user = User.query.get(user_id) 
    
    if not user:
        return jsonify({'message': 'User không tồn tại'}), 404
        
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}), 200
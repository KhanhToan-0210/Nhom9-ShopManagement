import jwt
from functools import wraps
from flask import request, jsonify
import os
import datetime

# Lấy cấu hình từ .env (đã được tải trong app.py)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRATION_DAYS = int(os.getenv('JWT_EXPIRATION_DAYS', 1))

def generate_jwt(user_id, role):
    """Tạo JWT Token"""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXPIRATION_DAYS),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'role': role
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

def token_required(f):
    """Decorator để yêu cầu Token hợp lệ cho các API"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Lấy token từ header Authorization
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token là bắt buộc!'}), 401

        try:
            # Giải mã token
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            # Lưu thông tin user vào request context
            request.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator để yêu cầu quyền ADMIN"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.current_user.get('role') != 'ADMIN':
            return jsonify({'message': 'Bạn không có quyền ADMIN để thực hiện thao tác này!'}), 403
        return f(*args, **kwargs)
    return decorated
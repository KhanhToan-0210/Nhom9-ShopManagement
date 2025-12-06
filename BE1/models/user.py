from app import db # Import đối tượng db đã được khởi tạo từ app.py
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'Users'
    
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # Lưu ý: password_hash là NULLable vì user có thể đăng nhập qua Google/FB
    password_hash = db.Column(db.String(255), nullable=True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Định nghĩa vai trò (role) sử dụng Enum
    role = db.Column(Enum('ADMIN', 'STAFF', 'CUSTOMER', name='user_role_enum'), 
                     nullable=False, 
                     default='STAFF')
                     
    google_id = db.Column(db.String(255), nullable=True)
    facebook_id = db.Column(db.String(255), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        """Chuyển đổi User object thành dictionary, loại trừ password_hash"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'google_id': self.google_id,
            'facebook_id': self.facebook_id,
            'is_active': self.is_active
        }
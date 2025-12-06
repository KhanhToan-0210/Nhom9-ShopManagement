from app import db
from sqlalchemy import DECIMAL

class Product(db.Model):
    __tablename__ = 'Products'
    
    id = db.Column(db.BigInteger, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'price': float(self.price), # Chuyển Decimal sang float để JSON hóa
            'is_visible': self.is_visible,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
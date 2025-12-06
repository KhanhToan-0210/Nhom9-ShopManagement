from app import db

class Customer(db.Model):
    __tablename__ = 'Customers'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob.isoformat() if self.dob else None,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
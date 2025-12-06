from flask import Blueprint, request, jsonify
from app import db
from models.customer import Customer
from utils.jwt_auth import token_required, admin_required

customer_bp = Blueprint('customer_bp', __name__)

# POST /api/customers (Thêm khách hàng mới) - Cần quyền ADMIN
@customer_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_customer():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'message': 'Tên khách hàng là bắt buộc'}), 400

    try:
        new_customer = Customer(
            name=data['name'],
            dob=data.get('dob'),
            address=data.get('address'),
            phone=data.get('phone')
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Khách hàng được tạo thành công!', 'customer': new_customer.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi CSDL: {str(e)}'}), 500

# GET /api/customers (Lấy danh sách)
@customer_bp.route('/', methods=['GET'])
@token_required
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200

# GET /api/customers/{id} (Lấy chi tiết)
@customer_bp.route('/<int:customer_id>', methods=['GET'])
@token_required
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Khách hàng không tồn tại'}), 404
    return jsonify(customer.to_dict()), 200


# PUT /api/customers/{id} (Cập nhật) - Cần quyền ADMIN
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
@admin_required
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Khách hàng không tồn tại'}), 404

    data = request.get_json()
    try:
        customer.name = data.get('name', customer.name)
        customer.dob = data.get('dob', customer.dob)
        customer.address = data.get('address', customer.address)
        customer.phone = data.get('phone', customer.phone)
        db.session.commit()
        return jsonify({'message': 'Cập nhật thành công!', 'customer': customer.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi CSDL: {str(e)}'}), 500

# GET /api/customers/search?q=keyword (Tìm kiếm khách hàng)
@customer_bp.route('/search', methods=['GET'])
@token_required
def search_customers():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'message': 'Vui lòng cung cấp từ khóa tìm kiếm (q)'}), 400
    
    # Tìm kiếm theo tên hoặc số điện thoại
    customers = Customer.query.filter(
        (Customer.name.ilike(f'%{query}%')) | (Customer.phone.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([c.to_dict() for c in customers]), 200
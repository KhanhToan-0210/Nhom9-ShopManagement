from flask import Blueprint, request, jsonify
from app import db
from models.product import Product
from utils.jwt_auth import token_required, admin_required

product_bp = Blueprint('product_bp', __name__)

# POST /api/products (Thêm sản phẩm mới) - Yêu cầu ADMIN
@product_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_product():
    data = request.get_json()
    if not all(key in data for key in ['sku', 'name', 'price']):
        return jsonify({'message': 'Thiếu thông tin bắt buộc (sku, name, price)'}), 400
    
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({'message': 'Mã SKU đã tồn tại.'}), 409

    try:
        new_product = Product(
            sku=data['sku'],
            name=data['name'],
            price=data['price'],
            is_visible=data.get('is_visible', True)
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Sản phẩm được tạo thành công!', 'product': new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi CSDL: {str(e)}'}), 500

# GET /api/products (Lấy danh sách)
@product_bp.route('/', methods=['GET'])
@token_required
def get_all_products():
    # Chỉ hiển thị sản phẩm đang 'visible' nếu người dùng không phải ADMIN
    # Để đơn giản, hiện tại chỉ lấy tất cả, nhưng bạn có thể thêm logic phân quyền tại đây.
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

# GET /api/products/search?q=keyword (Tìm kiếm sản phẩm)
@product_bp.route('/search', methods=['GET'])
@token_required
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'message': 'Vui lòng cung cấp từ khóa tìm kiếm (q)'}), 400
    
    # Tìm kiếm theo tên hoặc SKU
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | (Product.sku.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([p.to_dict() for p in products]), 200

# PUT /api/products/{id} (Cập nhật) - Yêu cầu ADMIN
@product_bp.route('/<int:product_id>', methods=['PUT'])
@token_required
@admin_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Sản phẩm không tồn tại'}), 404

    data = request.get_json()
    try:
        product.sku = data.get('sku', product.sku)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        db.session.commit()
        return jsonify({'message': 'Cập nhật thành công!', 'product': product.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi CSDL: {str(e)}'}), 500

# PATCH /api/products/{id}/visibility (Ẩn/Hiện sản phẩm) - Yêu cầu ADMIN
@product_bp.route('/<int:product_id>/visibility', methods=['PATCH'])
@token_required
@admin_required
def update_visibility(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Sản phẩm không tồn tại'}), 404

    data = request.get_json()
    isVisible = data.get('is_visible')

    if isVisible is None or not isinstance(isVisible, bool):
         return jsonify({'message': 'Giá trị is_visible (boolean) là bắt buộc.'}), 400

    try:
        product.is_visible = isVisible
        db.session.commit()
        return jsonify({'message': 'Cập nhật trạng thái hiển thị thành công!', 'is_visible': product.is_visible}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Lỗi CSDL: {str(e)}'}), 500
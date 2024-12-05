from flask import Blueprint, session, request, jsonify, render_template, flash, redirect, url_for
from models.product import Product
from models.category import Category
from models.comment import Comment
from models.order import Order
from models.order import OrderItem
from datetime import datetime
from sqlalchemy import or_


from extensions import db

api = Blueprint('api', __name__)

#Produkty
@api.route('/products', methods=['GET'])
def get_products():
    """Zwraca listę wszystkich produktów."""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Zwraca szczegóły konkretnego produktu."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

@api.route('/products', methods=['POST'])
def create_product():
    """Tworzy nowy produkt."""
    data = request.json
    product = Product(
        name=data.get('name'),
        category_id=data.get('category_id'),
        description=data.get('description'),
        price=data.get('price'),
        quantity=data.get('quantity'),
        image_url=data.get('image_url')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Usuwa produkt."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return '', 204

#Wyszukiwanie dynamiczne
@api.route('/search_products', methods=['GET'])
def search_products():
    """Wyszukuje produkty na podstawie zapytania."""
    query = request.args.get('query', '')

    # Wyszukiwanie produktów
    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{word}%')
            for word in query.split()
        )
    ).all()

    # Przygotowanie danych do formatu JSON
    products_data = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "image_url": product.image_url or "/static/images/default.png"
        }
        for product in products
    ]

    return jsonify(products_data), 200

#Kategorie
@api.route('/categories', methods=['GET'])
def get_categories():
    """Zwraca listę wszystkich kategorii."""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

#Komentarze
@api.route('/products/<int:product_id>/comments', methods=['GET'])
def get_comments(product_id):
    """Zwraca komentarze dla produktu."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    comments = product.comments
    return jsonify([comment.to_dict() for comment in comments]), 200

@api.route('/products/<int:product_id>/comments', methods=['POST'])
def add_comment(product_id):
    """Dodaje komentarz do produktu."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.json
    comment = Comment(
        product_id=product_id,
        user_name=data.get('user_name'),
        content=data.get('content')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

#Koszyk
@api.route('/cart', methods=['GET'])
def get_cart():
    """Zwraca koszyk użytkownika."""
    cart = session.get('cart', {})
    return jsonify(cart), 200

@api.route('/cart', methods=['POST'])
def add_to_cart():
    """Dodaje produkt do koszyka."""
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get(product_id)
    if not product or product.quantity < quantity:
        return jsonify({"error": "Product unavailable"}), 400

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity
        }
    session['cart'] = cart
    return jsonify(cart), 200

@api.route('/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    """Usuwa produkt z koszyka."""
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    return jsonify(cart), 200

@api.route('/cart', methods=['DELETE'])
def clear_cart():
    """Czyści koszyk."""
    session.pop('cart', None)
    flash('Koszyk został wyczyszczony', "info")
    return jsonify({"message": "Cart cleared"}), 200

#Zamówienia
@api.route('/orders', methods=['POST'])
def create_order():
    """Tworzy nowe zamówienie."""
    data = request.json
    cart = session.get('cart', {})
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    order = Order(
        user_id=data.get('user_id'),
        order_date=datetime.now(),
        total_price=total_price,
        status='Pending'
    )
    db.session.add(order)
    db.session.flush()

    for product_id, item in cart.items():
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=item['quantity'],
            price=item['price'] * item['quantity']
        )
        db.session.add(order_item)

    db.session.commit()
    session.pop('cart', None)
    return jsonify(order.to_dict()), 201
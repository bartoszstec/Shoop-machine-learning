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

#Dodawanie komentarza
@api.route('/products/<int:product_id>/addcomment', methods=['POST'])
def add_comment(product_id):
    """Dodaje komentarz do produktu."""
    data = request.json
    new_comment = Comment(
        product_id=product_id,
        user_name=data['user_name'],
        content=data['content'],
        classification=data['classification']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment.to_dict()), 201

#Wyświetlanie produktów danej kategorii
@api.route('/categories/<category_name>', methods=['GET'])
def get_category_with_products(category_name):
    category = Category.query.filter_by(category_name=category_name).first()
    if not category:
        return jsonify({"error": "Category not found"}), 404

    products = Product.query.filter_by(category_id=category.id).all()
    return jsonify({
        "category": category.to_dict(),
        "products": [product.to_dict() for product in products]
    }), 200

#Wyświetlanie szczegółów produktu
@api.route('/products/<product_id>', methods=['GET'])
def get_product_details(product_id):

    product = Product.query.get_or_404(product_id)
    comments = product.comments
    return jsonify({
        "product": product.to_dict(),
        "comments": [comment.to_dict() for comment in comments]
    }), 200
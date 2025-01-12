from flask import Blueprint, session, request, jsonify, render_template, flash, redirect, url_for
from models.product import Product
from models.category import Category
from models.comment import Comment
from models.order import Order, OrderItem
from sqlalchemy import or_
import joblib
import spacy
from sklearn.preprocessing import LabelEncoder
from extensions import db

api = Blueprint('api', __name__)

#label_encoder = LabelEncoder()

# Załaduj model i wektoryzator
model = joblib.load("model/rf_classifier.pkl")
tfidf_vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# Załaduj model językowy dla polskiego
nlp = spacy.load("pl_core_news_sm")

# Funkcja do lematyzacji
def lematyzuj_tekst(tekst):
    dokument = nlp(tekst)
    return " ".join([token.lemma_ for token in dokument if not token.is_punct and not token.is_space])

@api.route('/predict_comment_class', methods=['POST'])
def predict_comment_class():
    """Przewiduje klasyfikację komentarza na podstawie treści."""
    data = request.json

    try:
        data = request.json

        # Walidacja danych wejściowych
        if not all(key in data for key in ['content', 'category', 'product']):
            return jsonify({"error": "Brak wymaganych danych (content, category, product)."}), 400

        # Pobranie danych z żądania
        opinion_content = data['content']
        product_category = data['category']
        product_name = data['product']

        # Przetwarzanie danych
        lematyzowana_opinia = lematyzuj_tekst(opinion_content)
        cechy_wejsciowe = f"{product_category} {product_name} {lematyzowana_opinia}"
        wektor_cech = tfidf_vectorizer.transform([cechy_wejsciowe])

        # Predykcja klasy
        predicted_class = model.predict(wektor_cech)[0]

        return jsonify({"predicted_class": predicted_class}), 200
    
    except Exception as e:
        # Obsługa wyjątków i logowanie błędu
        print(f"Błąd podczas predykcji: {str(e)}")
        return jsonify({"error": "Wystąpił błąd podczas predykcji.", "details": str(e)}), 500


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

@api.route('/orders', methods=['GET'])
def get_user_orders():
    
    user_id = session['user_id']
    try:
        # Pobranie zamówień użytkownika
        orders = Order.query.filter_by(user_id=user_id).all()

        # Jeśli brak zamówień, zwróć pustą listę
        if not orders:
            return jsonify([]), 200

        # Konwersja zamówień na JSON
        orders_data = []
        for order in orders:
            orders_data.append({
                "id": order.id,
                "order_date": order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                "total_price": order.total_price,
                "status": order.status.value,
                "street": order.street,
                "city": order.city,
                "zip_code": order.zip_code,
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_name": Product.query.get(item.product_id).name,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order.items
                ]
            })
        return jsonify(orders_data), 200

    except Exception as e:
        return jsonify({"error": "Wystąpił błąd podczas pobierania zamówień.", "details": str(e)}), 500
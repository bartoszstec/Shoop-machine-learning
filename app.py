from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from extensions import db
from models.product import Product
from auth.auth import auth
from cart.cart import cart
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy

# Inicjalizacja aplikacji Flask i załadowanie pliku konfiguracyjnego
app = Flask(__name__)
app.config.from_object(Config)


# #Inicjalizacja SQLAlchemy
db.init_app(app)

# Rejestracja Blueprintów
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(cart, url_prefix='/cart')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/kategorie/<category_name>')
def show_category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    
    return render_template('category.html', category_name=category_name, products=products)

@app.route('/search_products', methods=['GET'])
def search_products():
    # Pobierz zapytanie z parametrów URL
    query = request.args.get('query', '')

    # Wyszukaj produkty na podstawie nazwy (ignorując wielkość liter)
    products = Product.query.filter(
    or_(
        Product.name.ilike(f'%{word}%')
        for word in query.split()
    )
).all()
    
    # Przygotuj dane produktów do formatu JSON
    products_data = [
        {
            "name": product.name,
            "price": product.price,
            "image_url": product.image_url  # lub "/static/images/default.png" dla braku obrazka
        }
        for product in products
    ]
    
    # Zwróć dane w formacie JSON
    return jsonify(products_data)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Musisz być zalogowany, aby zobaczyć tę stronę. Nie masz konta? Utwórz je klikając przycisk poniżej', "info")
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
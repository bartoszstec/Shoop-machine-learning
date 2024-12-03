from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from extensions import db
from models.product import Product
from models.comment import Comment
from models.category import Category
from auth.auth import auth
from cart.cart import cart
from sqlalchemy import or_

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
    category = Category.query.filter_by(category_name=category_name).first()

    if not category:
        # Jeśli kategoria nie istnieje, zwróć błąd 404
        return render_template('404.html'), 404

    products = Product.query.filter_by(category_id=category.id).all()
    
    return render_template('category.html', category_name=category_name, products=products)

@app.route('/product_details', methods=['GET', 'POST'])
def productDetails():
    product_id = request.args.get('product_id') if request.method == 'GET' else request.form.get('product_id')
    if not product_id:
        return redirect(url_for('index'))  # Jeśli brak ID, przekieruj na stronę główną
    
    # Pobierz produkt z bazy danych
    product = Product.query.get_or_404(product_id)
    comments = product.comments
    return render_template('product.html', product=product, comments=comments)

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
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "image_url": product.image_url  # lub "/static/images/default.png" dla braku obrazka
        }
        for product in products
    ]
    
    # Zwróć dane w formacie JSON
    return jsonify(products_data)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    # Sprawdź, czy użytkownik ma rolę "admin"
    if 'user_id' not in session:
        flash('Zaloguj się, aby dodać komentarz.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Pobierz dane z formularza
    product_id = request.form['product_id']
    user_name = request.form['user_name']
    content = request.form['content']
    
    # # Utwórz nowy komentarz
    new_comment = Comment(product_id=product_id, user_name=user_name, content=content)
    
    db.session.add(new_comment)
    db.session.commit()
    
    flash('Komentarz został opublikowany!', 'success')
    return redirect(url_for('productDetails', product_id=product_id))


if __name__ == '__main__':
    app.run()
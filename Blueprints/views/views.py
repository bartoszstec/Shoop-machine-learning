from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models.product import Product
from models.comment import Comment
from models.category import Category



views = Blueprint('views', __name__)

@views.route('/')
def index():
    """Strona główna."""
    return render_template('index.html')

@views.route('/kategorie/<category_name>')
def show_category(category_name):
    """Widok kategorii z listą produktów."""
    category = Category.query.filter_by(category_name=category_name).first()
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category_name=category_name, products=products)

@views.route('/product_details', methods=['GET', 'POST'])
def productDetails():
    product_id = request.args.get('product_id') if request.method == 'GET' else request.form.get('product_id')
    if not product_id:
        return redirect(url_for('views.index'))  # Jeśli brak ID, przekieruj na stronę główną
    
    # Pobierz produkt z bazy danych
    product = Product.query.get_or_404(product_id)
    comments = product.comments
    return render_template('product.html', product=product, comments=comments)

@views.route('/add_comment', methods=['POST'])
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
    return redirect(url_for('views.productDetails', product_id=product_id))
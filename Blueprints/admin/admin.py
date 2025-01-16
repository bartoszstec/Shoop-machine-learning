from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.person import Person
from models.product import Product
from models.category import Category
from models.order import Order, StatusEnum
from extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/adminpage')
def adminpage():
    # Sprawdź, czy użytkownik ma rolę "admin"
    if session.get('user_role') != 'admin':
        flash('Nie masz dostępu do tej strony.', 'error')
        return redirect(url_for('views.index'))
    
    # Pobierz listę wszystkich użytkowników
    users = Person.query.all()
    products = Product.query.all()
    categories = Category.query.all()
    orders = Order.query.all()
    
    for order in orders:
        for item in order.items:
            item.product_name = Product.query.filter_by(id=item.product_id).first().name

    return render_template('adminpage.html', users=users, products=products, categories=categories, orders=orders)

@admin.route('/change_role/<int:user_id>', methods=['POST'])
def change_role(user_id):
    # Sprawdź, czy użytkownik ma rolę "admin"
    if session.get('user_role') != 'admin':
        flash('Nie masz uprawnień do zmiany ról użytkowników.', 'error')
        return redirect(url_for('views.index'))
    
    # Pobierz nową rolę z formularza
    new_role = request.form['new_role']
    
    # Pobierz użytkownika z bazy danych
    user = Person.query.get(user_id)
    if user:
        # Zmień rolę użytkownika i zapisz w bazie
        user.role = new_role
        db.session.commit()
        flash(f'Rola użytkownika {user.login} została zmieniona na {new_role}.', 'success')
    else:
        flash('Nie znaleziono użytkownika.', 'error')
    
    return redirect(url_for('admin.adminpage') + '#users-section')

@admin.route('/update_order_status', methods=['POST'])
def update_order_status():
    # Sprawdź, czy użytkownik ma rolę "admin"
    if session.get('user_role') != 'admin':
        flash('Nie masz dostępu do tej strony.', 'error')
        return redirect(url_for('views.index'))
    
    order_id = request.form.get('order_id')

    if not order_id or not order_id.isdigit():
        flash('Nieprawidłowe ID zamówienia.', 'error')
        return redirect(url_for('admin.adminpage') + '#orders-section')
    
    # Znajdź zamówienie po ID
    order = Order.query.filter_by(id=int(order_id)).first()
    if not order:
        flash('Zamówienie nie zostało znalezione.', 'error')
        return redirect(url_for('admin.adminpage') + '#orders-section')
    
    if order.status == StatusEnum.pending:
        order.status = StatusEnum.completed
    else:
        order.status = StatusEnum.pending
    db.session.commit()
    flash('Status zamówienia został zaktualizowany.', 'success')
    return redirect(url_for('admin.adminpage') + '#orders-section')    

@admin.route('/add_product', methods=['POST'])
def add_product():
    # Sprawdź, czy użytkownik ma rolę "admin"
    if session.get('user_role') != 'admin':
        flash('Nie masz uprawnień do dodawania produktów.', 'error')
        return redirect(url_for('views.index'))
    
    # Pobierz dane z formularza
    name = request.form['name']
    category_id = request.form['category']
    description = request.form['description']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    image_url = request.form.get('image_url', None)
    
    # Utwórz nowy produkt
    new_product = Product(name=name, category_id=category_id, description=description,
                          quantity=quantity, price=price, image_url=image_url)
    
    db.session.add(new_product)
    db.session.commit()
    
    flash('Produkt został dodany pomyślnie!', 'success')
    
    # Przekieruj z powrotem do strony admina z parametrem "#products-section"
    return redirect(url_for('admin.adminpage') + '#products-section')
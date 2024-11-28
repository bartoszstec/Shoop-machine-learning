from flask import Blueprint, session, request, jsonify, render_template, flash, redirect, url_for
from models.product import Product
from models.order import Order, OrderItem
from extensions import db
from datetime import datetime

cart = Blueprint('cart', __name__)

@cart.route('/view_cart')
def view_cart():

    cart = session.get('cart', {})
    # Przelicz całkowitą cenę
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return render_template('cart.html', cart=cart, total_price=total_price)

@cart.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_price = float(request.form.get('product_price'))

    if 'user_id' not in session:
        flash('Musisz być zalogowany, aby zobaczyć tę stronę. Nie masz konta? Utwórz je klikając przycisk poniżej', "info")
        return jsonify({}), 401 #pusty json z kodem 401(brak autoryzacji)
    
     # Sprawdź dostępność produktu w bazie danych
    product = Product.query.get(product_id)
    if not product:
        flash('Produkt nie istnieje.', "danger")
        return jsonify({}), 404

    if product.quantity <= 0:
        flash('Produkt jest niedostępny.', "warning")
        return jsonify({}), 400

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if product_id in cart:
        # Sprawdź, czy dodanie kolejnej sztuki nie przekracza dostępności
        if cart[product_id]['quantity'] + 1 > product.quantity:
            flash('Brak wystarczającej ilości tego produktu w magazynie.', "warning")
            return jsonify({}), 400
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product_name,
            'price': product_price,
            'quantity': 1
        }
    
    session['cart'] = cart
    flash('Produkt został dodany do koszyka', "success")
    return jsonify(session['cart'])

@cart.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')

    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
    
    flash('Produkt został usunięty z koszyka', "info")
    return jsonify(session['cart'])

@cart.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Koszyk został wyczyszczony', "info")
    return jsonify()

@cart.route('/finalization', methods=['POST'])
def finalization():
    if 'user_id' not in session:
        flash('Musisz być zalogowany, aby złożyć zamówienie.', "info")
        return redirect(url_for('auth.login'))

    cart = session.get('cart', {})
    if not cart:
        flash('Koszyk jest pusty. Dodaj produkty, aby kontynuować.', "info")
        return redirect(url_for('index'))

    # Utwórz zamówienie
    order = Order(
        user_id=session['user_id'],
        order_date=datetime.now(),
        status='Pending'
    )
    db.session.add(order)
    db.session.flush()  # Pobiera ID zamówienia przed commitem

    for product_id, item in cart.items():
        product = Product.query.with_for_update().get(product_id)
        if not product or product.quantity < item['quantity']:
            flash(f'Produkt {item["name"]} jest niedostępny w wymaganej ilości.', "warning")
            return redirect(url_for('cart.view_cart'))

        # Zmniejsz stan magazynowy
        product.quantity -= item['quantity']

        # Aktualizuj cenę na podstawie bazy danych
        item['price'] = product.price

        # Dodaj pozycję zamówienia
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item['quantity'],
            price=item['price'] * item['quantity']
        )
        db.session.add(order_item)

    # Zapisz zmiany w bazie danych
    db.session.commit()

    # Wyczyść koszyk
    session.pop('cart', None)
    flash('Zamówienie zostało złożone pomyślnie.', "success")
    return redirect(url_for('cart.view_cart'))
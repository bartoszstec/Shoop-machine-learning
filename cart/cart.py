from flask import Blueprint, session, request, jsonify, render_template, flash, redirect, url_for

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

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if product_id in cart:
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
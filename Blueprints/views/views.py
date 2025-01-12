from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, abort
from extensions import db
from models.product import Product
from models.comment import Comment
from models.category import Category
import requests

views = Blueprint('views', __name__)

API_BASE_URL = "http://127.0.0.1:5000/api"

@views.route('/')
def index():
    """Strona główna."""
    return render_template('index.html')

@views.route('/kategorie/<category_name>')
def show_category(category_name):
    response = requests.get(f"{API_BASE_URL}/categories/{category_name}")
    if response.status_code == 404:
       abort(404)  # Wywołuje handler błędu 404

    data = response.json()
    return render_template('category.html', category_name=data["category"]["category_name"], products=data["products"])

@views.route('/product_details', methods=['GET', 'POST'])
def productDetails():
    product_id = request.args.get('product_id') if request.method == 'GET' else request.form.get('product_id')
    if not product_id:
        return redirect(url_for('views.index'))  # Jeśli brak ID, przekieruj na stronę główną
    
    response = requests.get(f"{API_BASE_URL}/products/{product_id}")
    if response.status_code == 404:
        abort(404)
    
    data = response.json()
    product = data["product"]
    comments = data["comments"]

    return render_template('product.html', product=product, comments=comments)

@views.route('/add_comment', methods=['POST'])
def add_comment_view():
    if 'user_id' not in session:
        flash('Zaloguj się, aby dodać komentarz.', 'warning')
        return redirect(url_for('auth.login'))
    
    product_id = request.form['product_id']
    user_name = request.form['user_name']
    content = request.form['content']
    classification = request.form['classification']
    product_category = request.form['category']
    product_name = request.form['product']
    
    response = requests.post(
        f"{API_BASE_URL}/products/{product_id}/addcomment",
        json={"user_name": user_name, "content": content, "classification": classification}
    )
    if response.status_code == 201:
        predict_response = requests.post(
            f"{API_BASE_URL}/predict_comment_class",
            json={
                "content": content,
                "category": product_category,
                "product": product_name
            }
        )
        if predict_response.status_code == 200:
            prediction = predict_response.json().get("predicted_class", "Nieznana")
            flash(f"Komentarz dodany! Model przewidział klasyfikację: {prediction}", "success")
        else:
            print("Błąd predykcji:", predict_response.json())  # Logowanie błędu
            flash("Komentarz dodany, ale nie udało się uzyskać predykcji.", "warning")
    else:
        flash("Nie udało się dodać komentarza.", "error")

    

    return redirect(url_for('views.productDetails', product_id=product_id))

@views.route('/myorders')
def view_user_orders():
    if 'user_id' not in session:
        flash('Zaloguj się, aby zobaczyć sowje zamówienia.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']

    # Wywołanie API lub zapytanie do bazy danych w celu pobrania zamówień użytkownika
    response = requests.get(f"{API_BASE_URL}/orders?user_id={user_id}")


    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    if response.status_code != 200:
        flash('Nie udało się pobrać zamówień. Spróbuj ponownie później.', 'error')
        return redirect(url_for('views.index'))

    # Zamówienia użytkownika
    orders = response.json()
    # Renderuj szablon z zamówieniami
    return render_template('user_orders.html', orders=orders)
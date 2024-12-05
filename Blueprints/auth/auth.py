from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.person import Person
from models.product import Product
from models.category import Category
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        
        # Szukanie użytkownika w bazie danych
        user = Person.query.filter_by(login=login).first()
        
        if user and user.check_password(password):
            # Zalogowanie użytkownika
            session['user_id'] = user.id
            session['user_login'] = user.login
            session['user_role'] = user.role
            flash('Zalogowano pomyślnie!', "success")
            return redirect(url_for('views.index'))
        else:
            flash('Niepoprawny login lub hasło.', "error")
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Sprawdzenie czy hasła są zgodne
        if password != confirm_password:
            flash('Hasła nie są zgodne!', "error")
            return redirect(url_for('auth.login'))
        
        # Sprawdzenie czy użytkownik już istnieje
        if Person.query.filter_by(login=login).first():
            flash('Użytkownik o podanym loginie już istnieje!', "error")
            return redirect(url_for('auth.login'))
        
        # Utworzenie nowego użytkownika
        new_user = Person(login=login, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Zarejestrowano pomyślnie! Możesz się zalogować.', "success")
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    session.pop('user_role', None)
    session.pop('cart', None)
    flash('Wylogowano pomyślnie.', "success")
    return redirect(url_for('auth.login'))

@auth.route('/adminpage')
def adminpage():
    # Sprawdź, czy użytkownik ma rolę "admin"
    if session.get('user_role') != 'admin':
        flash('Nie masz dostępu do tej strony.', 'error')
        return redirect(url_for('views.index'))
    
    # Pobierz listę wszystkich użytkowników
    users = Person.query.all()
    products = Product.query.all()
    categories = Category.query.all()
    
    return render_template('adminpage.html', users=users, products=products, categories=categories)

@auth.route('/change_role/<int:user_id>', methods=['POST'])
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
    
    return redirect(url_for('auth.adminpage') + '#users-section')

@auth.route('/add_product', methods=['POST'])
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
    return redirect(url_for('auth.adminpage') + '#products-section')
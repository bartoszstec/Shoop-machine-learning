from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.person import Person
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
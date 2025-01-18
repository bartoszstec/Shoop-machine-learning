from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.person import Person
from flask_mail import Message
from flask import url_for
from extensions import db, mail
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os

auth = Blueprint('auth', __name__)
# Konfiguracja serializer'a (do generowania tokenów)
serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'super_secret_key_change_me'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Szukanie użytkownika w bazie danych
        user = Person.query.filter_by(email=email).first()

        if not user.activated:
            flash('Twoje konto nie jest aktywne! Sprawdź swoją pocztę i potwierdź rejestrację.', "warning")
            return redirect(url_for('auth.confirm_email_page'))
        
        if user and user.check_password(password):
            # Zalogowanie użytkownika
            session['user_id'] = user.id
            session['user_login'] = user.login
            session['user_role'] = user.role
            flash('Zalogowano pomyślnie!', "success")
            return redirect(url_for('views.index'))
        else:
            flash('Niepoprawny email lub hasło.', "error")
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Sprawdzenie czy hasła są zgodne
        if password != confirm_password:
            flash('Hasła nie są zgodne!', "error")
            return redirect(url_for('auth.login'))
        
        # Sprawdzenie czy użytkownik już istnieje
        if Person.query.filter_by(email=email).first():
            flash('Użytkownik o podanym emailu już istnieje!', "error")
            return redirect(url_for('auth.login'))
        
        # Utworzenie nowego użytkownika
        new_user = Person(login=login, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        send_confirmation_email(email)

        
        flash('Konto zostało utworzone pomyślnie, sprawdź skrzynkę mailową i podaj kod do aktywacji konta', "success")
        return redirect(url_for('auth.confirm_email_page'))
    
    return render_template('login.html')

def send_confirmation_email(user_email):
    """Funkcja do wysyłania e-maila z potwierdzeniem"""
    user = Person.query.filter_by(email=user_email).first()
    if not user or user.activated:
        return  # Nie wysyłamy e-maila, jeśli użytkownik już aktywował konto
    
    token = serializer.dumps(user_email, salt="email-confirmation")
    user.set_confirmation_token(token)

    subject = "Potwierdzenie rejestracji"
    body = f"""
    Witaj,

    Aby potwierdzić swoje konto, skopiuj poniższy token:

    {token}

    Następnie przejdź na stronę: {url_for('auth.confirm_email_page', _external=True)}

    Pozdrawiamy,
    Twój Zespół
    """

    msg = Message(subject, recipients=[user_email], body=body)
    mail.send(msg)

@auth.route('/confirm-email', methods=['GET', 'POST'])
def confirm_email_page():
    if request.method == 'POST':
        token = request.form.get('token')

        if not token:
            flash('Token jest wymagany!', 'error')
            return redirect(url_for('auth.confirm_email_page'))

        try:
            email = serializer.loads(token, salt="email-confirmation", max_age=86400)
        except SignatureExpired:
            flash('Kod wygasł! Wyślij maila z kodem aktywacyjnym na swoją skrzynkę pocztową.', 'error')
            return redirect(url_for('auth.confirm_email_page'))
        except BadSignature:
            flash('Podany token jest nieprawidłowy. Sprawdź, czy skopiowałeś go poprawnie lub poproś o nowy.', 'error')
            return redirect(url_for('auth.confirm_email_page'))

        user = Person.query.filter_by(email=email).first()

        if not user:
            flash('Nie znaleziono użytkownika.', 'error')
            return redirect(url_for('auth.register'))

        # SPRAWDZENIE, CZY TOKEN JEST POPRAWNY
        if user.activated:
                flash('Konto jest już aktywne, zaloguj się.', 'info')
                return redirect(url_for('auth.login'))
        else:
            if user.confirmation_token and user.confirmation_token == token:
                user.activated = True
                user.confirmation_token = None
                db.session.commit()
                flash('Twoje konto zostało aktywowane!', 'success')

                return redirect(url_for('auth.login'))
            
        flash('Kod nieprawidłowy, spróbuj jeszcze raz!', 'error')
        return redirect(url_for('auth.confirm_email_page'))

    return render_template('confirm_email.html')

@auth.route('/resend-confirmation', methods=['POST'])
def resend_confirmation():
    email = request.form.get('email')

    if not email:
        flash("Podaj adres e-mail!", "warning")
        return redirect(url_for('auth.confirm_email_page'))

    user = Person.query.filter_by(email=email).first()

    if not user:
        flash("Nie znaleziono użytkownika z tym adresem e-mail.", "error")
        flash("Zarejestruj się lub wpisz poprawny email.", "info")
        return redirect(url_for('auth.confirm_email_page'))

    if user.activated:
        flash("To konto jest już aktywowane! Możesz się zalogować.", "info")
        return redirect(url_for('auth.login'))
    
    new_token = serializer.dumps(user.email, salt="email-confirmation")
    user.set_confirmation_token(new_token)

    # Ponowne wysłanie e-maila aktywacyjnego
    send_confirmation_email(user.email)
    flash("E-mail aktywacyjny został wysłany ponownie!", "success")

    return redirect(url_for('auth.confirm_email_page'))

@auth.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    session.pop('user_role', None)
    session.pop('cart', None)
    flash('Wylogowano pomyślnie.', "success")
    return redirect(url_for('auth.login'))
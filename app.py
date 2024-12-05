from flask import Flask, render_template
from config import Config
from extensions import db
from Blueprints.auth.auth import auth
from Blueprints.cart.cart import cart
from Blueprints.api.api import api
from Blueprints.views.views import views

# Inicjalizacja aplikacji Flask i załadowanie pliku konfiguracyjnego
app = Flask(__name__)
app.config.from_object(Config)


# #Inicjalizacja SQLAlchemy
db.init_app(app)

# Rejestracja Blueprintów
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(cart, url_prefix='/cart')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # W razie błędu w bazie danych
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
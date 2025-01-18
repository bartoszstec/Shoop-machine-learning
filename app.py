from flask import Flask, render_template
from config import Config
from extensions import db, mail
from Blueprints.auth.auth import auth
from Blueprints.cart.cart import cart
from Blueprints.api.api import api
from Blueprints.views.views import views
from Blueprints.admin.admin import admin

# Inicjalizacja aplikacji Flask i załadowanie pliku konfiguracyjnego
app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)


# #Inicjalizacja SQLAlchemy
db.init_app(app)

# Rejestracja Blueprintów
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(cart, url_prefix='/cart')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(views)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # W razie błędu w bazie danych
    return render_template('500.html', error=error), 500

if __name__ == '__main__':
    app.run()
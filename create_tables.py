from flask import Flask
from extensions import db
from models import Comment, Person, Product, Order, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/shoopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tabele zostały utworzone!")

# Przykładowe kategorie
# categories = ["AGD", "RTV", "Telefony", "Odzież", "Sport", "Zegarki i biżuteria"]

# for category_name in categories:
#     category = Category(category_name=category_name)
#     db.session.add(category)

#     db.session.commit()
#     print("Kategorie zostały dodane.")
from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer(), primary_key=True)  # ID produktu
    name = db.Column(db.String(255), nullable=False)  # Nazwa produktu
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) # Powiązanie z kategorią
    description = db.Column(db.Text, nullable=True)  # Opis produktu
    quantity = db.Column(db.Integer, nullable=False, default=0)  # Ilość sztuk na stanie
    price = db.Column(db.Float, nullable=False)  # Cena produktu
    image_url = db.Column(db.String(255), nullable=True)  # Opcjonalny URL obrazka produktu
    date_added = db.Column(db.DateTime, default=datetime.now)  # Data dodania produktu

    # Relacja do komentarzy
    comments = db.relationship('Comment', back_populates='product', cascade='all, delete-orphan')

    
    def to_dict(self):
        """Konwertuje obiekt Product na słownik."""
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
            "image_url": self.image_url,
            "date_added": self.date_added
        }
    
    def __repr__(self):
        return f"<Product {self.name} - {self.category}>"
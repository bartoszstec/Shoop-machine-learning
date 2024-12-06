from datetime import datetime
from extensions import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

     # Relacja z produktami
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        """Konwertuje obiekt Category na słownik."""
        return {
            "id": self.id,
            "category_name": self.category_name
        }

    def __repr__(self):
        return f"<Category {self.category_name}>"
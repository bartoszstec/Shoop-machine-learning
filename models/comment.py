from datetime import datetime
from extensions import db

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Powiązanie z produktem
    user_name = db.Column(db.String(50), nullable=False)  # Nazwa użytkownika
    content = db.Column(db.Text, nullable=False)  # Treść komentarza
    created_at = db.Column(db.DateTime, default=datetime.now)  # Data i czas dodania komentarza

    # Relacja odwrotna do modelu produktu
    product = db.relationship('Product', back_populates='comments')
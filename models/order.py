from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)  # ID zamówienia
    user_id = db.Column(db.Integer, nullable=False)  # ID użytkownika składającego zamówienie
    order_date = db.Column(db.DateTime, default=datetime.now)  # Data złożenia zamówienia
    status = db.Column(db.String(50), default='Pending')  # Status zamówienia (np. Pending, Completed)

    # Relacja do tabeli `order_item`
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id} - Status: {self.status}>"
    
class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)  # ID pozycji zamówienia
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)  # Powiązanie z tabelą `order`
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Powiązanie z tabelą `product`
    quantity = db.Column(db.Integer, nullable=False)  # Ilość produktu
    price = db.Column(db.Float, nullable=False)  # Cena jednostkowa produktu w momencie zakupu

    def __repr__(self):
        return f"<OrderItem Order ID: {self.order_id}, Product ID: {self.product_id}>"
from extensions import db
from datetime import datetime
from sqlalchemy import Enum
import enum


class StatusEnum(enum.Enum):
    pending = "Pending"
    completed = "Completed"

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)  # ID zamówienia
    user_id = db.Column(db.Integer, nullable=False)  # ID użytkownika składającego zamówienie
    order_date = db.Column(db.DateTime, default=datetime.now)  # Data złożenia zamówienia
    total_price = db.Column(db.Float, nullable=False) # Cena za całe zamówienie
    status = db.Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(50), nullable=False)


    # Relacja do tabeli `order_item`
    items = db.relationship(
        'OrderItem',
        backref='order',
        lazy=True,
        cascade="all, delete-orphan"
    )

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
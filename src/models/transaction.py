from src.extensions import db
from datetime import datetime
from sqlalchemy.orm import validates
import uuid

class Transaction(db.Model):
    __tablename__ = "transactions"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('TransactionItem', backref='transaction', lazy=True, cascade="all, delete-orphan")
    
    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['pending', 'completed', 'failed', 'refunded']
        if status not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return status
    
    @validates('total_amount')
    def validate_total_amount(self, key, amount):
        if amount < 0:
            raise ValueError('Total amount must be positive')
        return amount
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class TransactionItem(db.Model):
    __tablename__ = "transaction_items"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError('Quantity must be positive')
        return quantity
    
    @validates('price_at_time')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError('Price must be positive')
        return price
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_time': float(self.price_at_time)
        }
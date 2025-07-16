from __init__ import app, db
from datetime import datetime
import pandas as pd
from sqlalchemy.exc import IntegrityError
import logging

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True)  # Match CSV's ID format
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    aisle = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))

    # Optional: Link to users (for restock alerts)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='tracked_products')

    def __repr__(self):
        return f'Product(id={self.product_id}, name={self.name}, stock={self.stock})'

    # CRUD methods (same as before)
    def create(self): ...
    def read(self): ...
    def update(self, **kwargs): ...
    def delete(self): ...

def initProducts():
    """Load CSV data into SQLite once at startup"""
    with app.app_context():
        db.create_all()
        
        # Skip if DB already populated
        if Product.query.first():
            return

        try:
            df = pd.read_csv('walmart_inventory.csv')
            for _, row in df.iterrows():
                product = Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    stock=row['stock'],
                    aisle=row['aisle'],
                    price=row['price'],
                    category=row.get('category', 'general'),
                )
                db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to load CSV: {str(e)}")
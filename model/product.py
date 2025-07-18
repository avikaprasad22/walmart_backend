from __init__ import app, db
from datetime import datetime
import pandas as pd
from sqlalchemy.exc import IntegrityError
import logging

class Product(db.Model):
    __tablename__ = 'products'

    # Mirror your CSV columns exactly
    product_id = db.Column(db.String(50), primary_key=True)  # Assuming CSV has 'product_id' as a unique identifier
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    aisle = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Product(id={self.product_id}, name={self.name}, stock={self.stock})'

    # Simplified CRUD methods
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error creating product: {str(e)}")
            return None

    def read(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "stock": self.stock,
            "aisle": self.aisle,
            "price": self.price,
        }

def initProducts():
    """Load CSV data into SQLite once at startup"""
    with app.app_context():
        db.create_all()
        if Product.query.first():  # Skip if DB already has data
            return

        try:
            df = pd.read_csv('walmart_inventory.csv')
            for _, row in df.iterrows():
                product = Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    stock=row['stock'],
                    aisle=row['aisle'],
                    price=row['price'],                )
                db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to load CSV: {str(e)}")
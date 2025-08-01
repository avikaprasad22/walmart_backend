from __init__ import db, app
from model.product import Product
from model.user import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Wishlist model
class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String, db.ForeignKey('users._uid'), nullable=False)
    product_id = db.Column(db.String, db.ForeignKey('products.product_id'), nullable=False)
    date_added = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    notify = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='wishlist', lazy=True)
    product = db.relationship('Product', backref='wishlist', lazy=True, primaryjoin="Wishlist.product_id == Product.product_id")

    def __repr__(self):
        return f"<Wishlist(id={self.id}, user_uid={self.user_uid}, product_id={self.product_id}, notify={self.notify}, date_added={self.date_added})>"

    def read(self):
        return {
            "id": self.id,
            "user_uid": self.user_uid,
            "product_id": self.product_id,
            "product": self.product.read() if self.product else None,
            "availability": "in stock" if self.product and self.product.stock > 0 else "out of stock",
            "date_added": self.date_added.strftime('%Y-%m-%d'),
            "notify": self.notify
        }

    @classmethod
    def restore(cls, data):
        added_items = []
        with app.app_context():
            for record in data:
                try:
                    if 'date_added' in record and isinstance(record['date_added'], str):
                        record['date_added'] = datetime.strptime(record['date_added'], '%Y-%m-%d').date()
                    if 'id' in record:
                        del record['id']
                    wishlist_item = cls(**record)
                    db.session.add(wishlist_item)
                    added_items.append(wishlist_item)
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"Failed to restore Wishlist item: {record}. Error: {str(e)}")
            db.session.commit()
        return added_items

# Get wishlist for a user
def get_wishlist(user_uid):
    with app.app_context():
        return Wishlist.query.filter_by(user_uid=user_uid).all()

# Add a product to the wishlist
def add_to_wishlist(user_uid, product_id, notify=False):
    with app.app_context():
        try:
            existing = Wishlist.query.filter_by(user_uid=user_uid, product_id=product_id).first()
            if existing:
                return "Product already exists in the wishlist."

            item = Wishlist(user_uid=user_uid, product_id=product_id, notify=notify)
            db.session.add(item)
            db.session.commit()
            return f"Product with id {product_id} added to the wishlist."
        except IntegrityError:
            db.session.rollback()
            return f"Product with id {product_id} already exists in the wishlist."
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"

# Delete a product from the wishlist
def delete_from_wishlist(user_uid, product_id):
    with app.app_context():
        try:
            item = Wishlist.query.filter_by(user_uid=user_uid, product_id=product_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return f"Product with id {product_id} removed from the wishlist."
            else:
                return f"Product with id {product_id} not found in the wishlist."
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"

# Update notify field
def update_notify_flag(id, new_flag: bool):
    with app.app_context():
        try:
            item = Wishlist.query.get(id)
            if not item:
                return f"Wishlist item with id {id} not found."
            item.notify = new_flag
            db.session.commit()
            return f"Notification flag for wishlist item {id} updated to {new_flag}."
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"

# Initialize wishlist with seed data
def initWishlist():
    with app.app_context():
        db.create_all()

        sample_items = [
            Wishlist(user_uid='toby', product_id='1', notify=True),
            Wishlist(user_uid='toby', product_id='2', notify=False),
            Wishlist(user_uid='hop', product_id='3', notify=True),
        ]

        for item in sample_items:
            try:
                db.session.add(item)
                db.session.commit()
                logger.info(f"Wishlist item created: {repr(item)}")
            except IntegrityError:
                db.session.rollback()
                logger.warning(f"Duplicate or error: {repr(item)}")
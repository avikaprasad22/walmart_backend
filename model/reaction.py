from flask_restful import Api, Resource
from sqlalchemy import Text, JSON
from __init__ import app, db
from sqlalchemy import Column, Integer, String, Text
from sqlite3 import IntegrityError

# Reaction model definition
class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(String, db.ForeignKey('users.id'), nullable=False) #person
    post_id = db.Column(String, db.ForeignKey('posts.id'), nullable=False) #post
    reaction_type = db.Column(String, nullable=False) #reaction




    def __init__(self, reaction_type, user_id, post_id):
        self.reaction_type = reaction_type
        self.user_id = user_id
        self.post_id = post_id

    def add_reaction(reaction_type, user_id, post_id):
        new_reaction = Reaction(
            reaction_type=reaction_type,
            user_id=user_id,
            post_id=post_id
        )

        try:
            db.session.add(new_reaction)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return f"<Reaction {self.reaction_type}>"
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def read(self):
        """
        Retrieve the vote data as a dictionary.

        Returns:
            dict: Dictionary with vote information.
        """
        return {
            "reaction_type": self.reaction_type,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
    
    @staticmethod
    def restore(data):
        """
        Restores a list of suggested books from the provided data. If a book with the same
        title already exists, it updates it; otherwise, it creates a new one.

        Args:
            data (list): A list of dictionaries containing suggested book data.

        Returns:
            dict: A dictionary of restored suggested books (book id as keys).
        """
        restored_reactions = {}

        for reaction_data in data:
            # Remove 'id' from the data if it exists (because id will be auto-generated)
            _ = reaction_data.pop('id', None)

            # Check if the book already exists based on title
            existing_user_id = Reaction.query.filter_by(title=reaction_data.get("title")).first()
            if existing_user_id:
                # Update the existing book with new data
                existing_user_id.reaction_type = existing_user_id.get('reaction_type', existing_user_id.reaction_type)
                existing_user_id.user_id = existing_user_id.get('user_id', existing_user_id.user_id)
                existing_user_id.post_id = existing_user_id.get('post_id', existing_user_id.post_id)
        
                db.session.commit()
                restored_reactions[existing_user_id.id] = existing_user_id
            else:
                # Create a new suggested book
                new_book = Reaction(**existing_user_id)
                new_book.create()
                restored_reactions[new_book.id] = new_book

        return restored_reactions

# reaction data to insert
def initReactions(): 
    reactions_data = [
        "👍", "❤️", "😂", "🎉", "😢", "😡"
    ]  

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        # Optionally, add some test data (replace with actual values as needed)

    # Optionally, add some test data (replace with actual values as needed)
    reactions = [
        Reaction(user_id=1, reaction_type='😢', post_id=1),
        Reaction(user_id=1, reaction_type='❤️', post_id=1)
    ]
        
    for react in reactions:
        try:
            db.session.add(react)
            db.session.commit()
            print(f"Record created: {repr(react)}")
        except IntegrityError:
            db.session.rollback()
            print(f"Duplicate or error: {repr(react)}")


# # Create the tables and initialize data
# with app.app_context():
#     db.create_all()  # Create tables
#     initReactions()  # Initialize the comments data
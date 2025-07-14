from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from uuid import uuid4
from flask import request, jsonify

app = Flask(__name__)

# Mock Databases
books = []  # List to store books
user_activities = []  # List to store user activity

# =========================
# Book Management API
# =========================


# GET /api/books - Retrieve all books with optional filters
@app.route('/api/books', methods=['GET'])
def get_books():
    genre = request.args.get('genre')
    author = request.args.get('author')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    # Filter books based on query parameters
    filtered_books = books
    if genre:
        filtered_books = [b for b in filtered_books if b['genre'].lower() == genre.lower()]
    if author:
        filtered_books = [b for b in filtered_books if b['author'].lower() == author.lower()]
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_books = filtered_books[start:end]
    
    return jsonify({"books": paginated_books}), 200

# POST /api/books - Add a new book
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "author": data['author'],
        "description": data.get('description', ''),
        "genre": data.get('genre', 'Unknown'),
        "shared_by": data.get('shared_by', 'Anonymous'),
        "date_added": datetime.now().isoformat()
    }
    books.append(new_book)
    return jsonify(new_book), 201

# =========================
# User Activity API
# =========================

# GET /api/user/<user_id>/activity - Retrieve user activity
@app.route('/api/user/<user_id>/activity', methods=['GET'])
def get_user_activity(user_id):
    activity_type = request.args.get('type')
    limit = int(request.args.get('limit', 10))
    
    # Filter activity by user ID
    user_activity = [a for a in user_activities if a['user_id'] == user_id]
    
    # Filter by activity type if specified
    if activity_type:
        user_activity = [a for a in user_activity if a['type'] == activity_type]
    
    # Limit the results
    limited_activity = user_activity[:limit]
    return jsonify({"user_id": user_id, "activity": limited_activity}), 200

# POST /api/user/<user_id>/activity - Log user activity
@app.route('/api/user/<user_id>/activity', methods=['POST'])
def log_user_activity(user_id):
    data = request.json
    new_activity = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": data['type'],  # e.g., shared_book, comment, reading_history
        "book_id": data.get('book_id'),
        "details": data.get('details', {}),
        "timestamp": datetime.now().isoformat()
    }
    user_activities.append(new_activity)
    return jsonify(new_activity), 201

# =========================
# Run Flask Server
# =========================
if __name__ == '__main__':
    app.run(debug=True)

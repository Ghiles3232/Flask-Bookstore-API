# Import necessary modules and libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import wikipediaapi
import requests

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define the Book model for the database
class Book(db.Model):
    # Define columns for the Book table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)

# Define the Review model for the database
class Review(db.Model):
    # Define columns for the Review table
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

    # Insert example data into the Book table
    book1 = Book(title='To Kill a Mockingbird', author='Harper Lee', summary='A classic novel', genre='Fiction')
    book2 = Book(title='1984', author='George Orwell', summary='Dystopian fiction', genre='Science Fiction')

    # Add more books as needed...

    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()

# Define API routes

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    # Query all books from the database
    books = Book.query.all()
    # Convert book objects to a list of dictionaries
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author,
                  'summary': book.summary, 'genre': book.genre} for book in books]
    # Return the list of books as JSON
    return jsonify({'books': book_list})

# Route to get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Query a book by its ID
    book = Book.query.get(book_id)
    if book:
        # Create a dictionary with book information
        book_data = {'id': book.id, 'title': book.title, 'author': book.author,
                     'summary': book.summary, 'genre': book.genre}
        # Create a list of dictionaries with reviews for the book
        reviews_data = [{'user': review.user, 'rating': review.rating, 'comment': review.comment}
                        for review in book.reviews]
        # Return book information and reviews as JSON
        return jsonify({'book': book_data, 'reviews': reviews_data})
    else:
        # Return an error message if the book is not found
        return jsonify({'error': 'Book not found'}), 404

# Route to add books to the database
@app.route('/books', methods=['POST'])
def add_books():
    try:
        # Get JSON data from the request
        data = request.get_json()
        # Check if the request is valid
        if not data or 'books' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        # Extract book data from the request
        books_data = data['books']

        # Iterate through each book data and add it to the database
        for book_data in books_data:
            new_book = Book(
                title=book_data.get('title'),
                author=book_data.get('author'),
                summary=book_data.get('summary'),
                genre=book_data.get('genre')
            )

            db.session.add(new_book)

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Books added successfully'}), 201

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # Query a book by its ID
        book = Book.query.get(book_id)

        if not book:
            # Return an error message if the book is not found
            return jsonify({'error': 'Book not found'}), 404

        # Get JSON data from the request
        data = request.get_json()

        # Check if the request is valid
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400

        # Update book information with data from the request
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.summary = data.get('summary', book.summary)
        book.genre = data.get('genre', book.genre)

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Query a book by its ID
        book = Book.query.get(book_id)

        if not book:
            # Return an error message if the book is not found
            return jsonify({'error': 'Book not found'}), 404

        # Delete the book from the database
        db.session.delete(book)
        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Book deleted successfully'}), 200

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to add a review for a book
@app.route('/reviews', methods=['POST'])
def add_review():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if the request is valid
        if not data or 'book_id' not in data or 'user' not in data or 'rating' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        # Extract review data from the request
        book_id = data['book_id']
        user = data['user']
        rating = data['rating']
        comment = data.get('comment', None)

        # Query a book by its ID
        book = Book.query.get(book_id)

        if not book:
            # Return an error message if the book is not found
                        return jsonify({'error': 'Book not found'}), 404

        # Create a new review instance
        new_review = Review(user=user, rating=rating, comment=comment, book=book)

        # Add the new review to the database
        db.session.add(new_review)
        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Review added successfully'}), 201

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        # Query all reviews from the database
        reviews = Review.query.all()
        print(f"Total reviews: {len(reviews)}")
        # Convert review objects to a list of dictionaries
        review_list = [{'id': review.id, 'user': review.user, 'rating': review.rating,
                        'comment': review.comment, 'book_id': review.book_id} for review in reviews]

        # Return the list of reviews as JSON
        return jsonify({'reviews': review_list})

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to get reviews for a specific book by ID
@app.route('/reviews/<int:book_id>', methods=['GET'])
def get_reviews_for_book(book_id):
    try:
        # Query a book by its ID
        book = Book.query.get(book_id)

        if not book:
            # Return an error message if the book is not found
            return jsonify({'error': 'Book not found'}), 404

        # Query all reviews for the specified book from the database
        reviews = Review.query.filter_by(book_id=book_id).all()
        print(f"Reviews for book {book_id}: {len(reviews)}")
        # Convert review objects to a list of dictionaries
        review_list = [{'id': review.id, 'user': review.user, 'rating': review.rating,
                        'comment': review.comment, 'book_id': review.book_id} for review in reviews]

        # Return the list of reviews for the book as JSON
        return jsonify({'reviews': review_list})

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Route to get the top-rated books based on average ratings
@app.route('/books/top', methods=['GET'])
def get_top_books():
    try:
        # Query the top 5 books with the highest average ratings from the database
        top_books = db.session.query(Book, func.avg(Review.rating).label('avg_rating')) \
            .join(Review, Book.id == Review.book_id) \
            .group_by(Book.id) \
            .order_by(func.avg(Review.rating).desc()) \
            .limit(5) \
            .all()

        # Convert book objects and average ratings to a list of dictionaries
        top_books_list = [{'id': book.id, 'title': book.title, 'author': book.author,
                           'summary': book.summary, 'genre': book.genre, 'average_rating': avg_rating}
                          for book, avg_rating in top_books]

        # Return the list of top-rated books as JSON
        return jsonify({'top_books': top_books_list})

    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

# Function to get information about an author from Wikipedia
def get_author_info(author_name):
    try:
        # Make a GET request to the Wikipedia API
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{author_name.replace(' ', '_')}")

        # Raise an HTTPError for bad responses
        response.raise_for_status()

        # Extract relevant information from the JSON response
        summary = response.json().get('extract', '')

        # Create a dictionary with the extracted information
        author_info = {'author': author_name, 'summary': summary}

        # Return the author information as JSON
        return jsonify(author_info), 200

    except requests.RequestException as err:
        # Handle request exceptions and return an error message
        return jsonify({"error": f"Request Exception: {err}"}), 500

# Define the route to get information about an author
@app.route("/author/<author_name>", methods=["GET"])
def get_author_route(author_name):
    return get_author_info(author_name)

# Run the Flask app if the script is executed
if __name__ == '__main__':
    app.run(debug=True)


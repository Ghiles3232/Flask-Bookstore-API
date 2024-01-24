import pytest
from app import app, db, Book, Review

# test_add_review: Verifies the successful addition of a review, ensuring the review data is correctly stored in the database.

# test_get_books: Confirms the accurate retrieval of all books, checking if the API endpoint returns the expected book list.


@pytest.fixture
def test_app():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SADeprecationWarning")
def test_add_review(test_app, client):
    with test_app.app_context():  # Establish the application context
        # Prepare test data
        book = Book(title='Test Book', author='Test Author', genre='Test Genre')
        db.session.add(book)
        db.session.commit()

        review_data = {
            'book_id': book.id,
            'user': 'Test User',
            'rating': 5,
            'comment': 'Test Comment'
        }

        # Make a POST request to add a review
        response = client.post('/reviews', json=review_data)

        # Assertions
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Review added successfully'

        # Check if the review is added to the database
        review = Review.query.filter_by(user='Test User').first()
        assert review is not None
        assert review.rating == 5
        assert review.comment == 'Test Comment'

@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SADeprecationWarning")
def test_get_books(test_app, client):
    with test_app.app_context():  # Establish the application context
        # Prepare test data
        book1 = Book(title='Book 1', author='Author 1', genre='Genre 1')
        book2 = Book(title='Book 2', author='Author 2', genre='Genre 2')

        db.session.add_all([book1, book2])
        db.session.commit()

        # Make a GET request to retrieve all books
        response = client.get('/books')

        # Assertions
        assert response.status_code == 200
        data = response.get_json()
        assert 'books' in data
        assert isinstance(data['books'], list)
        assert len(data['books']) == 2  # Assuming two books are added in this test



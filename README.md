# Flask Bookstore API

This Flask application provides a RESTful API for managing books and their reviews. It allows users to perform CRUD operations on books, add reviews, and retrieve information about authors from Wikipedia.

## Requirements
- Python 3.x
- Flask
- Flask SQLAlchemy
- Wikipedia-API
- Requests

## Usage
1. Run the application by executing the script `app.py`.
2. Use any API testing tool (e.g., Postman) to interact with the API endpoints.

## API Endpoints

### Books
- **GET /books**: Get all books.
- **GET /books/{book_id}**: Get a specific book by ID.
- **POST /books**: Add one or more books.
- **PUT /books/{book_id}**: Update a book by ID.
- **DELETE /books/{book_id}**: Delete a book by ID.

### Reviews
- **GET /reviews**: Get all reviews.
- **GET /reviews/{book_id}**: Get reviews for a specific book by ID.
- **POST /reviews**: Add a review for a book.

### Top Rated Books
- **GET /books/top**: Get the top-rated books based on average ratings.

### Author Information
- **GET /author/{author_name}**: Get information about an author from Wikipedia.

## Database
- The application uses SQLite as the database with SQLAlchemy as the ORM.
- Two tables are defined: `Book` and `Review`.
- The `Book` table stores information about books, including title, author, summary, and genre.
- The `Review` table stores reviews for books, including user, rating, and comment.

## Error Handling
- The application handles errors gracefully and returns appropriate error messages and status codes.

## Running the Application
- Make sure to install the required Python packages before running the application.
- The application runs in debug mode by default for development purposes.

For any questions or feedback, please contact the developer at [Your Email].

**Developer:** Ghiles Asmani

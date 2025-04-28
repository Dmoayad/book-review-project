# Book Review API

This project implements a RESTful API for a book review system using Django and Django REST Framework.

## Features

*   User registration and JWT-based authentication (login/refresh tokens).
*   Password change functionality for authenticated users.
*   Browse books (list and detail views).
*   Admin users can Create, Update, and Delete books.
*   Authenticated users can add reviews to books.
*   View all reviews for a specific book.
*   Authenticated users can edit or delete their *own* reviews.

## Technical Stack

*   Python 3
*   Django 4+
*   Django REST Framework
*   djangorestframework-simplejwt (for JWT Authentication)
*   SQLite3 (default database)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd book_review_project
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file: `pip freeze > requirements.txt`)*

4.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations api
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up an admin username, email, and password.

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

The base URL for the API is `/api/`.

**Authentication:**

*   `POST /api/register/` - Register a new user.
    *   Body: `{ "username": "newuser", "email": "user@example.com", "password": "password123", "password2": "password123" }`
*   `POST /api/token/` - Login and obtain JWT access and refresh tokens.
    *   Body: `{ "username": "testuser", "password": "password123" }`
*   `POST /api/token/refresh/` - Obtain a new access token using a refresh token.
    *   Body: `{ "refresh": "your_refresh_token" }`
*   `PUT /api/change-password/` - Change the logged-in user's password. (Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
    *   Body: `{ "old_password": "current_password", "new_password": "new_strong_password", "new_password2": "new_strong_password" }`

**Book Management:**

*   `GET /api/books/` - List all books.
*   `POST /api/books/` - Add a new book. (Admin only, Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
    *   Body: `{ "title": "New Book Title", "author": "Author Name", "description": "Book description." }`
*   `GET /api/books/<id>/` - Retrieve details of a specific book.
*   `PUT /api/books/<id>/` - Edit a book. (Admin only, Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
    *   Body: `{ "title": "Updated Title", ... }`
*   `DELETE /api/books/<id>/` - Delete a book. (Admin only, Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`

**Review Management:**

*   `GET /api/books/<book_id>/reviews/` - Get all reviews for a specific book.
*   `POST /api/books/<book_id>/reviews/` - Add a review to a specific book. (Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
    *   Body: `{ "rating": 5, "comment": "This book was amazing!" }`
*   `GET /api/reviews/<id>/` - Retrieve a specific review. (Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
*   `PUT /api/reviews/<id>/` - Edit a review. (Review owner only, Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`
    *   Body: `{ "rating": 4, "comment": "Updated thoughts." }`
*   `DELETE /api/reviews/<id>/` - Delete a review. (Review owner only, Requires Authentication)
    *   Header: `Authorization: Bearer <your_access_token>`

## Authentication Mechanism

This API uses JSON Web Tokens (JWT) for authentication, implemented via the `djangorestframework-simplejwt` library.

1.  Register a user using the `/api/register/` endpoint.
2.  Obtain an access token and a refresh token by sending the user's credentials (username and password) to the `/api/token/` endpoint.
3.  Include the access token in the `Authorization` header for all protected requests:
    `Authorization: Bearer <your_access_token>`
4.  Access tokens expire after a set time (default: 5 minutes). Use the refresh token with the `/api/token/refresh/` endpoint to get a new access token without needing to log in again.

## Testing Endpoints

You can test the endpoints using tools like `curl` or Postman.

**Example using `curl` (Login):**

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}' \
http://127.0.0.1:8000/api/token/

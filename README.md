# KeySavvy

KeySavvy is an e-commerce platform designed to offer a seamless shopping experience for users. The project uses Flask for the backend and a combination of HTML, CSS, and JavaScript for the frontend.

## Features

- **User Authentication**: Secure user authentication using Flask, Flask-WTF, WTForms, and Flask-SQLAlchemy. SQLAlchemy is used to manage the user database and handle authentication.
- **Product Listings**: Browse through a range of products with detailed descriptions.
- **Shopping Cart**: Add items to your cart and proceed to checkout.
- **Order Management**: Track and manage your orders efficiently.

## Technologies Used

### Backend
- **Flask**: A lightweight WSGI web application framework in Python.
- **Flask-WTF**: Simple integration of Flask and WTForms.
- **WTForms**: Forms handling in Flask, including validation.
- **Flask-SQLAlchemy**: SQLAlchemy integration with Flask.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.

### Frontend
- **HTML5**: The structure of the web pages.
- **CSS3**: Styling of the web pages.
- **JavaScript**: Dynamic behavior and interactions on the site.

## Installation

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.x
- Flask==2.0.2
- Flask-WTF==0.15.1
- WTForms==2.3.3
- Flask-SQLAlchemy==2.5.1

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/maxgoldberg25/KeySavvy.git
    cd KeySavvy
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install Flask==2.0.2 Flask-WTF==0.15.1 WTForms==2.3.3 Flask-SQLAlchemy==2.5.1
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

6. Open your browser and visit `http://127.0.0.1:5000`.

## Usage

- Register as a new user or log in with your existing account.
- Browse through the product listings.
- Add items to your cart and proceed to checkout.
- Track your order history from your account dashboard.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your proposed changes.

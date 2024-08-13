from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(60))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# for all products to be placed in database
class ProductAll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image = db.Column(db.String(255))  # Assuming image file path or URL
    

    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image


class Product(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image = db.Column(db.String(255))  # Assuming image file path or URL
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, price, image, user_id):
        self.name = name
        self.price = price
        self.image = image
        self.user_id = user_id

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

    def __repr__(self):
        return f"<Feedback {self.id}>"
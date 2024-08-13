from flask import Flask, render_template, redirect, request, url_for, flash
from models import db
from models import users, Product, ProductAll, Feedback
from forms import FeedbackForm
from flask import session



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


# Create the database tables
with app.app_context():
    db.create_all()

cart_items = []

products = [
        {'id': 1, 'title': 'Razer BlackWidow RGB', 'image': 'razer.png', 'price': '149.99'},
        {'id': 2, 'title': 'Logitech MX Mechanical', 'image': 'logitech.png', 'price': '89.99'},
        {'id': 3, 'title': 'Apple Magic Keyboard', 'image': 'mac.png', 'price': '299.99'},
        {'id': 4, 'title': 'Ducky One 2 Mini', 'image': 'ducky.png', 'price': '109.99'},
        {'id': 5, 'title': 'Keychron K2', 'image': 'keychron.png', 'price': '89.99'},
        {'id': 6, 'title': 'HyperX Alloy Core', 'image': 'hyperx.png', 'price': '49.99'},
        {'id': 7, 'title': 'SteelSeries Apex 3', 'image': 'steelseries.png', 'price': '49.99'},
        {'id': 8, 'title': 'Corsair K70 RGB', 'image': 'corsair.png', 'price': '159.99'},
        {'id': 9, 'title': 'Asus ROG Strix Flare', 'image': 'asus.png', 'price': '169.99'},
        {'id': 10, 'title': 'Cooler Master CK552', 'image': 'cooler_master.png', 'price': '79.99'},
        {'id': 11, 'title': 'HP 400 Wired', 'image': 'hp.png', 'price': '29.99'}
]

def add_products_to_database(products):
    for product_info in products:
        # Extract product information from the dictionary
        name = product_info['title']
        image = product_info['image']
        price = float(product_info['price'])

        # Create a new Product object
        product = ProductAll(name=name, image=image, price=price)

        # Add the product to the database session
        db.session.add(product)
        print(f'Added product: {name} - ${price:.2f}') # Remove this line after testing

    # Commit the changes to the database
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product')
def product():
    
        # Query the database to get all products
    # products = ProductAll.query.all()
    return render_template('product.html', products=products)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    # Find the product with the given product_id
    for product in products:
        if product['id'] == product_id:
            # Render the product_details.html template with the fetched product details
            return render_template('product_details.html', product=product)
    
    # If product is not found, return a 404 error
    return render_template('404.html'), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists
        existing_user = users.query.filter_by(name=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            # Create a new user
            new_user = users(name=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('index'))

    return render_template("signup.html")



@app.route("/login", methods=['POST', 'GET'])
def login():
    if "user" in session:
        flash('Already Logged In')
        return redirect(url_for("product"))

    if request.method == 'POST':
        session.permanent = True
        email = request.form["email"]
        session['user'] = email

        found_user = users.query.filter_by(email=email).first()

        if found_user:
            session["email"] = found_user.email
            flash('Login Successful')
            return redirect(url_for("product"))
        else:
            flash('User does not exist, please try again.')

    return render_template("login.html")

@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if "user" in session:
        username = session['user']  # Get the username from the session
        if request.method == 'POST':
            email = request.form.get('email')
            if email:
                session['email'] = email
                found_user = users.query.filter_by(name=username).first()
                if found_user:
                    found_user.email = email
                    db.session.commit()
                    flash('Email updated successfully')
                else:
                    flash('User not found')
            else:
                flash('Email cannot be empty')
        else:
            if 'email' in session:
                email = session['email']

        return render_template('user.html', email=email)
    else:
        flash('Login Unsuccessful')
        return redirect(url_for('login'))
    
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/clear_users', methods=['POST'])
def clear_users():
    try:
        # Delete all user records from the database
        db.session.query(users).delete()
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        flash('An error occurred while clearing the list of users: {}'.format(str(e)))

    return render_template("view.html")
    

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if request.method == 'POST':
        # Retrieve the product ID from the form data
        product_id = request.form.get('product_id')

        # Check if the product ID is valid
        if product_id:
            # Check if the product exists in the database
            product = ProductAll.query.get(product_id)
            if product:
                # If the product exists, create a new Product object and add it to the database
                new_product = Product(name=product.name, price=product.price, image=product.image, user_id=None)
                db.session.add(new_product)
                db.session.commit()
                cart_items.append(product_id)
                # print(f'Added product to cart: {product.name} - ${product.price:.2f}')

                # Flash a success message
                flash('Product added to cart successfully', 'success')
            else:
                # If the product does not exist, flash an error message
                flash('Product not found', 'error')
        else:
            # If no product ID is provided, flash an error message
            flash('Invalid product ID', 'error')

    # Redirect back to the product page after processing the form submission
    return redirect(url_for('product'))


# Flask route to retrieve cart items
@app.route('/cart')
def view_cart():
    # Query the database to fetch all products
    all_products = Product.query.all() # All_procucts is a list of all products in the cart
    cart_item_ids = session.get('cart', []) # FIXME doesn't get right money 

    # Filter out the products that are in the cart
    cart_products = [product for product in all_products]

    # Calculate subtotal
    subtotal = sum(product.price for product in cart_products)
    # Query the database to fetch details of the cart items
    
    print(subtotal)


    return render_template('cart.html', cart_items=all_products, subtotal=subtotal)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    try:
        # Delete all products in cart from the database
        db.session.query(Product).delete()
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        flash('An error occurred while clearing the list of products: {}'.format(str(e)))

    return render_template("cart.html")


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        # Create a new Feedback object and populate it with form data
        feedback_entry = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        # Add the feedback entry to the database session and commit
        db.session.add(feedback_entry)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))  # Redirect to avoid form resubmission on refresh
    return render_template('feedback.html', form=form)
    
@app.route('/feedback_results')
def feedback_results():
    feedback = Feedback.query.all()  # Query the database to retrieve all feedback entries
    print(feedback)
    return render_template('feedback_results.html', feedback=feedback)


if __name__ == '__main__':
    with app.app_context():
        add_products_to_database(products)

    app.run(debug=True)
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

import flask_login
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from grocery_app.__init__  import bcrypt
from flask_login import login_user, logout_user, login_required, current_user

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################
@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    #  Create a GroceryStoreForm
    form = GroceryStoreForm()
    
    if form.validate_on_submit():
        store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=flask_login.current_user
        )
        db.session.add(store)
        db.session.commit()
        # - flash a success message, and
    # - redirect the user to the store detail page.

        flash('Store Created.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    
    # Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()
    #  If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    if form.validate_on_submit():
        item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=flask_login.current_user
        )
        db.session.add(item)
        db.session.commit()
            # - flash a success message, and
        # - redirect the user to the store detail page.

        flash('Item added.')
        return redirect(url_for('main.store_detail', store_id=item.store.id))

    # : Send the form to the template and use it to render the form fields
    else:
        return render_template('new_item.html', form=form)


@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    # Create a GroceryItemForm

    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    #  If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        # - flash a success message, and
    # - redirect the user to the store detail page.

        flash('Store Updated.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', form=form, store=store)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    user = flask_login.current_user
    item = GroceryItem.query.get(item_id)

    user.shopping_list_items.append(item)
    db.session.add(user)
    db.session.commit()        
    flash('item added.')       
    return redirect(url_for('main.shopping_list'))

@main.route('/shopping_list')
@login_required
def shopping_list():
    user = flask_login.current_user
    return render_template('list_detail.html', user=user)
    

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    #  If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        # - flash a success message, and
    # - redirect the user to the store detail page.
        db.session.add(item)
        db.session.commit()
        flash('item Updated.')
        print('updated!')
        return redirect(url_for('main.item_detail', item_id=item.id))

    # Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)

# routes.py

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


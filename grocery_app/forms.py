from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app.models import GroceryStore, ItemCategory, User
from grocery_app.__init__ import bcrypt

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    title = StringField('Grocery Store', validators = [DataRequired()])
    # - address - StringField
    address = StringField('Address')
    # - submit button
    submit = SubmitField('Submit')
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    name = StringField('Name', validators=[DataRequired()])
    # - price - FloatField
    price = FloatField('Price')
    # - category - SelectField (specify the 'choices' param)
    category = SelectField('Category', choices=ItemCategory.choices())
    # - photo_url - StringField
    photo_url = StringField('Image URL', validators=[DataRequired()])
    # - store - QuerySelectField (specify the `query_factory` param)
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query.all(), get_label = 'title', allow_blank=False)
    # - submit button
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
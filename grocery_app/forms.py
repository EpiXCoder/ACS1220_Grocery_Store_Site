from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore, ItemCategory

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

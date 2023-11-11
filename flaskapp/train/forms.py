from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import SelectField, DateField, StringField
from wtforms.validators import DataRequired, ValidationError

class TicketMetaForm(FlaskForm):
    source_station = SelectField("Source", validators=[DataRequired()])
    destination_station = SelectField("Destination", validators=[DataRequired()])
    book_on = DateField("Departure Date")

    def validate_book_on(form, field):
        today = datetime.now().date()
        if field.data < today:
            raise ValidationError("Please select a date in the future.")

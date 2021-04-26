from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EditOrderForm(FlaskForm):
    delivery_date = DateField('Дата доставки', validators=[DataRequired()])
    about = TextAreaField("Пожелания о доставке или товаре")
    taken = BooleanField('Товар доставлен')
    submit = SubmitField('Submit')
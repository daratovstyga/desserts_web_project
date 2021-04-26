from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class NewOrderForm(FlaskForm):
    delivery_date = DateField('Дата доставки', validators=[DataRequired()])
    about = TextAreaField("Пожелания о доставке или товаре")
    submit = SubmitField('Submit')
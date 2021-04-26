from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired


class RateForm(FlaskForm):
    rating = StringField('Сколько по 10 бальной шкале заслуживает товар?', validators=[DataRequired()])
    about = TextAreaField("Оставьте нам ваш отзыв о товаре и доставке")
    submit = SubmitField('Submit')
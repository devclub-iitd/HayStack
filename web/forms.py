from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Query', render_kw={'placeholder':'Enter search query'},validators=[DataRequired()])
    submit = SubmitField('Use Magnet!')


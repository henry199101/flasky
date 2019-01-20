from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content')
    submit = SubmitField('Post Your Article !')

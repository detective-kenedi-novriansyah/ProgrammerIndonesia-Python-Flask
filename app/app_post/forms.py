from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class RecordPost(FlaskForm):
    id = IntegerField()
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
from wtforms import TextAreaField,StringField,SelectMultipleField,SelectField
from wtforms.validators import DataRequired,length
from flask_wtf import FlaskForm
from application.models import *


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), length(max=255)])
    text = TextAreaField('Content', [DataRequired()])
    categories = SelectField('Categories', coerce=int)

    def __init__(self):
        super(PostForm, self).__init__()
        self.categories.choices = [(c.id, c.name) for c in Species.query.order_by('id')]
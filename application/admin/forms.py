from wtforms import TextAreaField,StringField,SelectMultipleField,SelectField
from wtforms.validators import DataRequired,length
from flask_wtf import FlaskForm


class PostForm(FlaskForm):
    title = StringField('作业标题', [DataRequired(), length(max=255)])
    text = TextAreaField('作业内容', [DataRequired()])
    categories = SelectField('作业标签', coerce=int)
    describe = StringField('作业描述', [DataRequired(), length(max=255)])
    difficulty = SelectField('作业难度', coerce=str)

    def __init__(self):
        super(PostForm, self).__init__()
        from application.models import Species
        self.categories.choices = [(c.id, c.name) for c in Species.query.order_by('id')]
        dif = ['炼气','筑基','旋照','融合','心动','灵寂','元婴','出窍','分神','合体','度劫','大乘','渡劫']
        self.difficulty.choices = [(name,name) for name in dif]
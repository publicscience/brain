from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import Required

# No longer in use
class TrainingForm(Form):
    doc = TextAreaField('Text', validators=[Required()])


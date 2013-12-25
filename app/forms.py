from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import Required

class TweetingForm(Form):
    tweet = TextAreaField('Text', validators=[Required()])

# No longer in use
class TrainingForm(Form):
    doc = TextAreaField('Text', validators=[Required()])


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class ContactOwnerForm(FlaskForm):
    """Form for contacting the owner of a lost item."""
    post_id = HiddenField('Post ID', validators=[DataRequired()])
    finder_name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    finder_email = StringField('Your Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[
        DataRequired(), 
        Length(min=10, max=500, message="Please provide more details about the found item")
    ], render_kw={"placeholder": "Please describe where/when you found this item and how the owner can contact you."})
    submit = SubmitField('Contact Owner')

class ItemStatusForm(FlaskForm):
    """Form for updating item status (found/still lost)."""
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Update Status')

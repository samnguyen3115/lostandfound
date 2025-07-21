from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.main.models import User
from app import db
import sqlalchemy as sqla
from flask_login import current_user

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=500)])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalars(sqla.select(User).where(User.username == username.data)).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.scalars(sqla.select(User).where(User.email == email.data)).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

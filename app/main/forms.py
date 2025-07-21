from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from .models import Tag

from app import db
import sqlalchemy as sqla

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    body = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1500)])
    
    color_tag = QuerySelectField(
        'Color Tag',
        query_factory=lambda: db.session.scalars(sqla.select(Tag).where(Tag.category == "color").order_by(Tag.name)),  
        get_label=lambda tag: tag.name.title(),  
        allow_blank=True,
        blank_text='Select a color'
    )

    building_tag = QuerySelectField(
        'Building Tag',
        query_factory=lambda: db.session.scalars(sqla.select(Tag).where(Tag.category == "building").order_by(Tag.name)),  
        get_label=lambda tag: tag.name.replace('_', ' ').title(),  
        allow_blank=True,  
        blank_text='Select a building'
    )

    image = FileField('Please add an image of the item', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])    
    submit = SubmitField('Post')

class FilterForm(FlaskForm):
    color_filter = QuerySelectField(
        'Filter By Color',
        query_factory=lambda: db.session.scalars(sqla.select(Tag).where(Tag.category == "color").order_by(Tag.name)),
        get_label=lambda tag: tag.name.title(),
        allow_blank=True,
        blank_text='All Colors'
    )
    
    building_filter = QuerySelectField(
        'Filter By Building',
        query_factory=lambda: db.session.scalars(sqla.select(Tag).where(Tag.category == "building").order_by(Tag.name)),
        get_label=lambda tag: tag.name.replace('_', ' ').title(),
        allow_blank=True,
        blank_text='All Buildings'
    )
    
    submit = SubmitField('Filter')
    submit2 = SubmitField('Refresh')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=1, max=100)], 
                       render_kw={"placeholder": "Search for lost items..."})
    submit = SubmitField('Search')
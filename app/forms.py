"""
WTForms for the application
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class BlogForm(FlaskForm):
    """Form for creating and updating blog posts"""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=100, message='Title must be between 5 and 100 characters')
        ],
        render_kw={'placeholder': 'Enter blog title'}
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required'),
            Length(min=10, message='Content must be at least 10 characters')
        ],
        render_kw={'placeholder': 'Write your blog content here...', 'rows': 8}
    )
    submit = SubmitField('Publish Blog')

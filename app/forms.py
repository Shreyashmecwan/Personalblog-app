"""
WTForms for the Personal Blog Application

Forms for creating/editing blog content and user profiles.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CreatePostForm(FlaskForm):
    """Form for creating new blog posts"""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters')
        ],
        render_kw={'placeholder': 'Enter your blog title', 'class': 'form-control'}
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required'),
            Length(min=10, message='Content must be at least 10 characters')
        ],
        render_kw={
            'placeholder': 'Write your blog content here...',
            'rows': 10,
            'class': 'form-control'
        }
    )
    submit = SubmitField('Publish Post', render_kw={'class': 'btn btn-primary'})


class UpdatePostForm(FlaskForm):
    """Form for updating existing blog posts"""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters')
        ],
        render_kw={'placeholder': 'Enter your blog title', 'class': 'form-control'}
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required'),
            Length(min=10, message='Content must be at least 10 characters')
        ],
        render_kw={
            'placeholder': 'Write your blog content here...',
            'rows': 10,
            'class': 'form-control'
        }
    )
    submit = SubmitField('Update Post', render_kw={'class': 'btn btn-primary'})


class ProfileForm(FlaskForm):
    """Form for updating user profile"""
    full_name = StringField(
        'Full Name',
        validators=[
            Optional(),
            Length(min=2, max=120, message='Name must be between 2 and 120 characters')
        ],
        render_kw={'placeholder': 'Enter your full name', 'class': 'form-control'}
    )
    bio = TextAreaField(
        'Bio',
        validators=[
            Optional(),
            Length(max=500, message='Bio must not exceed 500 characters')
        ],
        render_kw={
            'placeholder': 'Tell us about yourself...',
            'rows': 5,
            'class': 'form-control'
        }
    )
    submit = SubmitField('Update Profile', render_kw={'class': 'btn btn-primary'})

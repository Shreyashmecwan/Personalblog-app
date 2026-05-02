"""
Database models for the application
"""
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """User model for authentication and blog ownership"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Blog post model"""
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'


class UserProfile(db.Model):
    """User profile model for additional user information"""
    __tablename__ = 'user_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<UserProfile {self.name}>'


class Comment(db.Model):
    """Comment model for blog post comments"""
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment on Post {self.post_id}>'


class Like(db.Model):
    """Like/Dislike model for blog posts"""
    __tablename__ = 'like'
    
    id = db.Column(db.Integer, primary_key=True)
    is_like = db.Column(db.Boolean, default=True)  # True for like, False for dislike
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    
    # Unique constraint to ensure one reaction per user per post
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post'),)
    
    def __repr__(self):
        return f'<Like by User {self.user_id} on Post {self.post_id}>'


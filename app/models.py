"""
Database models for the Personal Blog application

Models:
- User: User account and authentication
- UserProfile: Extended user profile information
- Post: Blog posts
- PostComment: Comments on blog posts
- PostReaction: User reactions (likes/dislikes) on posts
"""
from datetime import datetime
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """User account model for authentication and blog ownership"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='select', cascade='all, delete-orphan')
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='author', lazy='select', cascade='all, delete-orphan')
    reactions = db.relationship('PostReaction', backref='user', lazy='select', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    """Extended user profile information"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProfile {self.full_name}>'


class Post(db.Model):
    """Blog post model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('PostComment', backref='post', lazy='select', cascade='all, delete-orphan')
    reactions = db.relationship('PostReaction', backref='post', lazy='select', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def get_like_count(self):
        """Get total number of likes"""
        return PostReaction.query.filter_by(post_id=self.id, is_like=True).count()
    
    def get_dislike_count(self):
        """Get total number of dislikes"""
        return PostReaction.query.filter_by(post_id=self.id, is_like=False).count()
    
    def get_user_reaction(self, user_id):
        """Get user's reaction to this post"""
        reaction = PostReaction.query.filter_by(post_id=self.id, user_id=user_id).first()
        if reaction:
            return 'like' if reaction.is_like else 'dislike'
        return None


class PostComment(db.Model):
    """User comments on blog posts"""
    __tablename__ = 'post_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PostComment on Post {self.post_id}>'


class PostReaction(db.Model):
    """User reactions (likes/dislikes) on blog posts"""
    __tablename__ = 'post_reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    is_like = db.Column(db.Boolean, default=True, nullable=False)  # True for like, False for dislike
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Ensure one reaction per user per post
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_reaction'),)
    
    def __repr__(self):
        return f'<PostReaction {self.user_id} on Post {self.post_id}>'


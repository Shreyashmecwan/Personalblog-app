"""
Main routes (home page, profile)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Post, UserProfile

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """
    Display home page with all blog posts
    """
    posts = Post.query.all()
    userprofile = None
    
    if current_user.is_authenticated:
        userprofile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    return render_template('home.html', posts=posts, userprofile=userprofile)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and update user profile
    """
    user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        
        if not name or not email:
            flash('Name and email are required.', 'danger')
            return redirect(url_for('main.profile'))
        
        if user_profile:
            user_profile.name = name
            user_profile.email = email
            user_profile.bio = bio
        else:
            user_profile = UserProfile(
                name=name,
                email=email,
                bio=bio,
                user_id=current_user.id
            )
            db.session.add(user_profile)
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating profile.', 'danger')
        
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', profile=user_profile)

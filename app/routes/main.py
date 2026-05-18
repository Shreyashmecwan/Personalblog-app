"""
Main routes for home page and user profile management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Post, UserProfile
from app.forms import ProfileForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Display home page with paginated blog posts (5 per page, latest first)"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    user_profile = None
    
    if current_user.is_authenticated:
        user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    return render_template('home.html', posts=posts, profile=user_profile)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Display and update user profile"""
    user_profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm()
    
    if form.validate_on_submit():
        if not user_profile:
            user_profile = UserProfile(user_id=current_user.id)
            db.session.add(user_profile)
        
        user_profile.full_name = form.full_name.data
        user_profile.bio = form.bio.data
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'danger')
    elif request.method == 'GET' and user_profile:
        form.full_name.data = user_profile.full_name
        form.bio.data = user_profile.bio
    
    return render_template('profile.html', form=form, profile=user_profile)

"""
Utility routes for comments and reactions (likes/dislikes)
"""
from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import date
from app import db
from app.models import Post, Comment, Like

utils_bp = Blueprint('utils', __name__)


# ======================== COMMENT ROUTES ========================

@utils_bp.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    """
    Add a comment to a blog post
    """
    post = Post.query.get_or_404(post_id)
    
    content = request.form.get('comment_content', '').strip()
    
    if not content:
        flash('Comment cannot be empty!', 'danger')
        return redirect(url_for('blog.get_full_blog', post_id=post_id))
    
    try:
        new_comment = Comment(
            content=content,
            date=date.today().strftime("%d-%m-%Y"),
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()
        
        flash('Comment added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding your comment.', 'danger')
    
    return redirect(url_for('blog.get_full_blog', post_id=post_id))


@utils_bp.route('/delete_comment/<int:comment_id>/<int:post_id>', methods=['GET'])
@login_required
def delete_comment(comment_id, post_id):
    """
    Delete a comment (only by the comment author or post author)
    """
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    
    # Check authorization - allow comment author or post author to delete
    if comment.author != current_user and post.author != current_user:
        flash('You do not have permission to delete this comment.', 'danger')
        return redirect(url_for('blog.get_full_blog', post_id=post_id))
    
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the comment.', 'danger')
    
    return redirect(url_for('blog.get_full_blog', post_id=post_id))


# ======================== LIKE/DISLIKE ROUTES ========================

@utils_bp.route('/toggle_like/<int:post_id>', methods=['POST'])
@login_required
def toggle_like(post_id):
    """
    Toggle like for a blog post
    """
    post = Post.query.get_or_404(post_id)
    
    # Check if user already has a reaction
    existing_like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()
    
    try:
        if existing_like:
            # If user already liked, remove the like
            if existing_like.is_like:
                db.session.delete(existing_like)
                db.session.commit()
            else:
                # If user disliked, change to like
                existing_like.is_like = True
                existing_like.date = date.today().strftime("%d-%m-%Y")
                db.session.commit()
        else:
            # Add new like
            new_like = Like(
                is_like=True,
                user_id=current_user.id,
                post_id=post_id,
                date=date.today().strftime("%d-%m-%Y")
            )
            db.session.add(new_like)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your like.', 'danger')
    
    # Redirect back to the referring page or home
    return redirect(request.referrer or url_for('main.home'))


@utils_bp.route('/toggle_dislike/<int:post_id>', methods=['POST'])
@login_required
def toggle_dislike(post_id):
    """
    Toggle dislike for a blog post
    """
    post = Post.query.get_or_404(post_id)
    
    # Check if user already has a reaction
    existing_like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()
    
    try:
        if existing_like:
            # If user already disliked, remove the dislike
            if not existing_like.is_like:
                db.session.delete(existing_like)
                db.session.commit()
            else:
                # If user liked, change to dislike
                existing_like.is_like = False
                existing_like.date = date.today().strftime("%d-%m-%Y")
                db.session.commit()
        else:
            # Add new dislike
            new_dislike = Like(
                is_like=False,
                user_id=current_user.id,
                post_id=post_id,
                date=date.today().strftime("%d-%m-%Y")
            )
            db.session.add(new_dislike)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your dislike.', 'danger')
    
    # Redirect back to the referring page or home
    return redirect(request.referrer or url_for('main.home'))


@utils_bp.route('/get_reactions/<int:post_id>', methods=['GET'])
def get_reactions(post_id):
    """
    Get like and dislike counts for a post, and user's current reaction
    """
    post = Post.query.get_or_404(post_id)
    
    like_count = len([l for l in post.likes if l.is_like])
    dislike_count = len([l for l in post.likes if not l.is_like])
    
    user_reaction = None
    if current_user.is_authenticated:
        user_like = Like.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first()
        if user_like:
            user_reaction = 'like' if user_like.is_like else 'dislike'
    
    return jsonify({
        'like_count': like_count,
        'dislike_count': dislike_count,
        'user_reaction': user_reaction
    })

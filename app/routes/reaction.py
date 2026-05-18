"""
Routes for user interactions with blog posts.

Includes:
- Comment management (add, delete)
- Reaction management (likes/dislikes on posts)
"""
from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.models import Post, PostComment, PostReaction

reaction_bp = Blueprint('reaction', __name__)


# ======================== COMMENT ROUTES ========================

@reaction_bp.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a blog post"""
    post = Post.query.get_or_404(post_id)
    
    content = request.form.get('comment_content', '').strip()
    
    if not content:
        flash('Comment cannot be empty!', 'danger')
        return redirect(url_for('blog.get_full_blog', post_id=post_id))
    
    try:
        new_comment = PostComment(
            content=content,
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


@reaction_bp.route('/delete_comment/<int:comment_id>/<int:post_id>', methods=['GET'])
@login_required
def delete_comment(comment_id, post_id):
    """Delete a comment (by comment author or post author only)"""
    comment = PostComment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
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


# ======================== REACTION ROUTES (LIKE/DISLIKE) ========================

@reaction_bp.route('/toggle_like/<int:post_id>', methods=['POST'])
@login_required
def toggle_like(post_id):
    """Toggle like reaction on a blog post"""
    post = Post.query.get_or_404(post_id)
    
    existing_reaction = PostReaction.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()
    
    try:
        if existing_reaction:
            if existing_reaction.is_like:
                # Remove like if already liked
                db.session.delete(existing_reaction)
            else:
                # Change dislike to like
                existing_reaction.is_like = True
                existing_reaction.created_at = datetime.utcnow()
        else:
            # Add new like
            new_reaction = PostReaction(
                is_like=True,
                user_id=current_user.id,
                post_id=post_id
            )
            db.session.add(new_reaction)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your like.', 'danger')
    
    return redirect(request.referrer or url_for('main.home'))


@reaction_bp.route('/toggle_dislike/<int:post_id>', methods=['POST'])
@login_required
def toggle_dislike(post_id):
    """Toggle dislike reaction on a blog post"""
    post = Post.query.get_or_404(post_id)
    
    existing_reaction = PostReaction.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()
    
    try:
        if existing_reaction:
            if not existing_reaction.is_like:
                # Remove dislike if already disliked
                db.session.delete(existing_reaction)
            else:
                # Change like to dislike
                existing_reaction.is_like = False
                existing_reaction.created_at = datetime.utcnow()
        else:
            # Add new dislike
            new_reaction = PostReaction(
                is_like=False,
                user_id=current_user.id,
                post_id=post_id
            )
            db.session.add(new_reaction)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your dislike.', 'danger')
    
    return redirect(request.referrer or url_for('main.home'))


@reaction_bp.route('/get_reactions/<int:post_id>', methods=['GET'])
def get_reactions(post_id):
    """Get reaction counts and user's current reaction for a post"""
    post = Post.query.get_or_404(post_id)
    
    like_count = post.get_like_count()
    dislike_count = post.get_dislike_count()
    
    user_reaction = None
    if current_user.is_authenticated:
        user_reaction = post.get_user_reaction(current_user.id)
    
    return jsonify({
        'like_count': like_count,
        'dislike_count': dislike_count,
        'user_reaction': user_reaction
    })

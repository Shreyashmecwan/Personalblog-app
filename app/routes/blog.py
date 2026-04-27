"""
Blog routes (create, read, update, delete posts)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from datetime import date
from app import db
from app.models import Post
from app.forms import BlogForm

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    """
    Create a new blog post
    """
    form = BlogForm()
    
    if form.validate_on_submit():
        try:
            new_post = Post(
                title=form.title.data,
                content=form.content.data,
                date=date.today().strftime("%d-%m-%Y"),
                user_id=current_user.id
            )
            db.session.add(new_post)
            db.session.commit()
            
            flash('Blog post published successfully!', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the post.', 'danger')
    
    return render_template('create_blog.html', form=form)


@blog_bp.route('/get_full_blog/<int:post_id>', methods=['GET'])
def get_full_blog(post_id):
    """
    Display a single blog post
    """
    post = Post.query.get_or_404(post_id)
    return render_template('ShowBlog.html', post=post)


@blog_bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    """
    Update an existing blog post
    """
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.author != current_user:
        abort(403)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('blog.update', post_id=post_id))
        
        try:
            post.title = title
            post.content = content
            db.session.commit()
            
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the post.', 'danger')
    
    return render_template('update.html', post=post)


@blog_bp.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete(post_id):
    """
    Delete a blog post
    """
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.author != current_user:
        abort(403)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the post.', 'danger')
    
    return redirect(url_for('main.home'))

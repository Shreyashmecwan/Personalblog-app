"""
Blog post routes for CRUD operations.

Includes:
- Create blog posts
- Read/view blog posts
- Update blog posts
- Delete blog posts
"""
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.forms import CreatePostForm, UpdatePostForm

blog_bp = Blueprint('blog', __name__)


def save_post_image(image_file):
    """Save uploaded image and return filename"""
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        # Generate unique filename with timestamp
        import uuid
        filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_file.save(os.path.join(upload_folder, filename))
        return filename
    return None


def delete_post_image(filename):
    """Delete image file from server"""
    if filename:
        try:
            filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting image: {e}")


@blog_bp.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    """Create a new blog post"""
    form = CreatePostForm()
    
    if form.validate_on_submit():
        try:
            image_filename = None
            if form.image.data:
                image_filename = save_post_image(form.image.data)
            
            new_post = Post(
                title=form.title.data,
                content=form.content.data,
                category=form.category.data,
                image_filename=image_filename,
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
    """Display a single blog post"""
    post = Post.query.get_or_404(post_id)
    return render_template('ShowBlog.html', post=post)


@blog_bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    """Update an existing blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.author != current_user:
        abort(403)
    
    form = UpdatePostForm()
    
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.content = form.content.data
            post.category = form.category.data
            
            if form.image.data:
                # Delete old image if exists
                if post.image_filename:
                    delete_post_image(post.image_filename)
                # Save new image
                post.image_filename = save_post_image(form.image.data)
            
            db.session.commit()
            
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('blog.get_full_blog', post_id=post_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the post.', 'danger')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
    
    return render_template('update.html', form=form, post=post)


@blog_bp.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    """Delete a blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.author != current_user:
        abort(403)
    
    try:
        # Delete image if exists
        if post.image_filename:
            delete_post_image(post.image_filename)
        
        db.session.delete(post)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the post.', 'danger')
    
    return redirect(url_for('main.home'))

"""
Personal Blog Application Entry Point

Run this file to start the Flask development server:
    python run.py

The application will be available at http://localhost:5000
"""
from app import create_app, db

# Create Flask application instance
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make models available in flask shell"""
    from app.models import User, Post, UserProfile, PostComment, PostReaction
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'UserProfile': UserProfile,
        'PostComment': PostComment,
        'PostReaction': PostReaction,
    }


if __name__ == '__main__':
    app.run(debug=True)

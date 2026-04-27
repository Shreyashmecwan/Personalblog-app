"""
Application entry point
Run this file to start the Flask development server

Usage:
    python run.py
"""
import os
from app import create_app, db

# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': __import__('app.models', fromlist=['User']).User,
        'Post': __import__('app.models', fromlist=['Post']).Post,
        'UserProfile': __import__('app.models', fromlist=['UserProfile']).UserProfile,
    }


if __name__ == '__main__':
    app.run(debug=True)

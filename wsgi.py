"""
WSGI entry point for production deployment

Usage with Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

Usage with uWSGI:
    uwsgi --http :8000 --wsgi-file wsgi.py --callable app
"""
import os
from app import create_app, db

app = create_app(os.environ.get('FLASK_ENV', 'production'))


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
    app.run()

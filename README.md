# Personal Blog

A simple, clean blog application built with Flask for managing and sharing blog posts.

## Features

- **User Authentication**: Register, login, and manage accounts
- **Blog Management**: Create, read, update, and delete blog posts
- **Comments**: Add and manage comments on blog posts
- **Reactions**: Like and dislike blog posts
- **User Profiles**: Customize your profile with bio and personal information
- **Responsive Design**: Mobile-friendly user interface

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3
- **Authentication**: Flask-Login, Flask-Bcrypt

## Project Structure

```
PersonalBlog/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms
│   ├── routes/               # Route blueprints
│   │   ├── auth.py           # Authentication routes
│   │   ├── blog.py           # Blog post routes
│   │   ├── main.py           # Home & profile routes
│   │   └── reaction.py       # Comments & reactions
│   ├── static/               # CSS, JavaScript
│   └── templates/            # HTML templates
├── instance/                 # Instance-specific files (DB)
├── config.py                 # Configuration
├── run.py                    # Entry point
└── requirements.txt          # Dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PersonalBlog
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

The application will start at `http://localhost:5000`

## Database

The application uses SQLite for development. The database file (`dev_blog.db`) is automatically created in the `instance/` directory on first run.

### Database Schema

- **users**: User accounts
- **user_profiles**: Extended profile information
- **posts**: Blog posts
- **post_comments**: Comments on posts
- **post_reactions**: Likes/dislikes on posts

## Development

To debug or develop:

1. Ensure debug mode is enabled in `config.py` (default for development)
2. The Flask development server auto-reloads on code changes
3. Access the Flask shell:
   ```bash
   flask shell
   ```

## License

This project is open source and available under the MIT License.



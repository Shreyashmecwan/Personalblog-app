from flask import Flask, abort, render_template,url_for,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin , LoginManager, current_user , login_required , logout_user , login_user 
from flask_bcrypt import Bcrypt 
import datetime



app = Flask(__name__)
bycrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish Blog')

class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable=False )
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    posts = Post.query.all()
    
    return render_template('home.html' , posts=posts)

@app.route('/create_blog' , methods=[ 'GET', 'POST'])
@login_required
def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        new_post = Post(author=current_user,title=form.title.data,content=form.content.data,date=datetime.date.today().strftime("%d-%m-%Y"))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_blog.html' , form=form)



@app.route('/get_full_blog/<int:post_id>' , methods=['GET'])
def get_full_blog(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('ShowBlog.html' , post=post)
    


@app.route('/delete/<int:post_id>' , methods=['GET'])
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route('/update/<int:post_id>' , methods=['GET','POST'])
@login_required
def update(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html',post=post)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hash_password = bycrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=name,email=email,password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=[ 'GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bycrypt.check_password_hash( user.password , password ) :
            login_user(user)
            flash('Logged in Successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


 

if __name__ == "__main__":

    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user,login_required, logout_user, current_user
import os 
file_path = os.path.abspath(os.getcwd())+"\database.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = "hahaha"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class Post(db.Model):##create the Postform
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    
class User(UserMixin, db.Model):##create the userform
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class LoginForm(FlaskForm):##login form
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),  Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):##register form
    email =StringField('email', validators =[InputRequired(),Email(message = 'Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),  Length(min=8,max=80)])


@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return 'Invalid username or password'
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET','POST'])
def signUp():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New user has been created </h1>'
    return render_template('register.html', form=form)

@app.route('/dashboard/')
@login_required
def dashboard():
	return render_template('dashboard.html', name = current_user.username, email = current_user.email)

@app.errorhandler(404)
def page_not_fund(e):
        return render_template("404.html")
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/messages/',methods=['GET','POST']  )
@login_required
def messages():
    if request.method =='POST':
        post = Post(title=request.form['title'], content= request.form['content'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('messages.html')
if __name__ == '__main__':
	app.run()

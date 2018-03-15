##pre_forum_post 帖子表，pre_forum_thread 主题表
##pre_common_member 用户主表，pre_common_member_profile 用户栏目表
##pre_ucenter_pm_lists, 站内信列表， 具体的信息需要查看 pre_ucenter_pm_messages_0-9
from flask import Flask, render_template, redirect, url_for, request, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = "hahaha"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''#默认MySQL 配置
app.config['MYSQL_DB'] = 'ultrax'
Bootstrap(app)
mysql=MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    info = ['''SELECT * FROM pre2018_common_member''','''SELECT * FROM pre2018_forum_post''',
            '''SELECT * FROM pre2018_ucenter_pm_lists''']
    member=[]
    post=[]
    messages=[]
    memberName =[]
    memberEmail =[]
    author =[]
    subject =[]
    znxSubject=[]
    showResult=[[],[],[]]
    for i in range(0,len(info)):
        cur.execute(info[i])  #加入所有信息
        showResult[i]= cur.fetchall()
    for i in range (0, len(showResult[0])):
        member.append(str(showResult[0][i]))
        memberName.append (member[i].split(',')[2])#用户信息
        memberEmail.append(member[i].split(',')[1])
    for i in range (0, len(showResult[1])):
        post.append(str(showResult[1][i]))
        author.append (post[i].split(',')[4])#帖子信息
        subject.append(post[i].split(',')[6])
    for i in range (0, len(showResult[2])):
        messages.append(str(showResult[2][i]))#站内信信息
        znxSubject.append (messages[i].split(',')[3])
    
    return render_template("index.html", name = memberName, email = memberEmail, aut = author,
                           sub = subject, znxSub = znxSubject)

class LoginForm(FlaskForm):##login form
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),  Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):##register form
    email =StringField('email', validators =[InputRequired(),Email(message = 'Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),  Length(min=8,max=80)])

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session.pop('user',None)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pre2018_common_member WHERE username ='"+ form.username.data+"'")
        user = cur.fetchone()
        if user:
            if user[3]== form.password.data: ##check_password_hash(user[3], form.password.data: use sha256!!!
                session['user'] = form.username.data
                return redirect(url_for('dashboard'))
        return 'Invalid username or password'
    return render_template('login.html', form=form)

    
@app.route('/register/', methods=['GET','POST'])
def signUp():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        cur = mysql.connection.cursor()
        cur.execute('''SELECT MAX(uid) FROM pre2018_common_member''' )
        maxid = cur.fetchone()
        cur.execute('''INSERT INTO pre2018_common_member(uid,email,username,password) VALUES(%s,%s,%s,%s)''',
                    (maxid[0]+1,form.email.data,form.username.data,form.password.data ))
                    #discuz password 数据库无法放下sha256, 所以只能放原来的密码了
        mysql.connection.commit()
        return '<h1> New user has been created </h1>'
    return render_template('register.html', form=form)
@app.route('/dashboard/')
def dashboard():
    if g.user:
      return render_template('dashboard.html')
    return redirect(url_for('login'))
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.errorhandler(404)
def page_not_fund(e):
    return render_template("404.html")

@app.route('/logout/')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

    
if __name__ =='__main__':
     app.run(debug=True)

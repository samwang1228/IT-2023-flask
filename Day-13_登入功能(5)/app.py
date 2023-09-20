from flask import Flask, g,request,redirect,render_template
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)

 
app.config['DATABASE'] = 'test.db'
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/' 
login_manager = LoginManager()
login_manager.init_app(app)
SQLITE_DB_PATH = 'test.db'
SQLITE_DB_SCHEMA = 'test.sql'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    return user

@login_manager.request_loader
def request_loader(request):

    user_id = request.form.get('ID')

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!

    return user if (request.form['password'] == password[0][0]) else None

@app.route('/login', methods=['GET', 'POST']) #登入
def login():
    btn_check=None
    if request.method == 'GET':
        return render_template("login.html")


    user_id = request.form['ID']
    user_password = request.form['password']
    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()
    if not password:
        errorMsg='<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號不存在'
        return render_template('login.html', errorMsg = errorMsg)

    password = password[0][0]
    
    if user_password != password:
        errorMsg='<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號或密碼有誤'
        return render_template('login.html', errorMsg = errorMsg)
    user = User()
    user.id = user_id 
    login_user(user)
    username = current_user.get_id()
    return render_template('index.html',user_id=username)
@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = current_user.get_id()
    return render_template('index.html',user_id=user_id)
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')

    user_id = request.form['ID']
    user_password = request.form['password']
    check_passowrd= request.form.get('checkpassword')

    if(user_password != check_passowrd):
        errorMsg='<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的密碼有誤'
        return render_template('signup.html', errorMsg = errorMsg)

    db = get_db()

    try:
        with db:
            db.execute (
                'INSERT INTO members (account, password) VALUES (?, ?)',
                (user_id, user_password)
            )
    except sqlite3.IntegrityError:
        errorMsg='<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>該帳號已有人使用'
        return render_template('signup.html', errorMsg = errorMsg)
    user=User()
    user.id=user_id
    login_user(user)
    user_id = current_user.get_id() 
    return render_template('index.html',user_id=user_id)
@app.route('/logout')
def logout():
    logout_user()  # 登出用戶
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
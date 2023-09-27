from flask import Blueprint, render_template, redirect, request,url_for
from flask_login import login_user, logout_user, current_user,UserMixin,login_required
from backend.db import get_db
import sqlite3
SQLITE_DB_PATH='test.db' 

auth_bp = Blueprint('auth', __name__,template_folder='auth_templates')
class User(UserMixin):
    pass
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['ID']
    user_password = request.form['password']
    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id,)
    ).fetchone()

    if not password:
        errorMsg = '<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號不存在'
        return render_template('login.html', errorMsg=errorMsg)

    password = password[0]

    if user_password != password:
        errorMsg = '<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號或密碼有誤'
        return render_template('login.html', errorMsg=errorMsg)

    user = User()
    user.id = user_id
    login_user(user)
    username = current_user.get_id()
    return render_template('index.html', user_id=username)

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    user_id = current_user.get_id()
    return render_template('index.html', user_id=user_id)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')

    user_id = request.form['ID']
    user_password = request.form['password']
    check_password = request.form.get('checkpassword')

    if user_password != check_password:
        errorMsg = '<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的密碼有誤'
        return render_template('signup.html', errorMsg=errorMsg)

    db = get_db()

    try:
        with db:
            db.execute(
                'INSERT INTO members (account, password) VALUES (?, ?)',
                (user_id, user_password)
            )
    except sqlite3.IntegrityError:
        errorMsg = '<span style="color:#35858B"></span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>該帳號已有人使用'
        return render_template('signup.html', errorMsg=errorMsg)

    user = User()
    user.id = user_id
    login_user(user)
    user_id = current_user.get_id()
    return render_template('index.html', user_id=user_id)

@auth_bp.route('/logout')
def logout():
    logout_user()  # 登出用戶
    return redirect('/login')
@auth_bp.route('/manager', methods=['GET', 'POST'])
@login_required
def manager():
    user = current_user.get_id()
    if user != 'user':
        return redirect(url_for('index'))

    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    return render_template('manager.html', user=user, data=result, size=size)
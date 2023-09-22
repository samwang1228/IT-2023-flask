from flask import Flask, g,request,redirect,render_template,url_for,jsonify
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import secrets



app = Flask(__name__)

 
app.config['DATABASE'] = 'test.db'
app.secret_key = secrets.token_hex(16)
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
@app.route('/manager', methods=['GET', 'POST'])  # 登入
def manager():
    user = current_user.get_id()
    if user != 'user':
        return redirect(url_for('index'))

    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    return render_template('manager.html', user=user, data=result, size=size)
from flask import jsonify

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user = current_user.get_id()
    user_id = request.form['username']
    db = get_db()
    try:
        with db:
            db.execute(
                'DELETE FROM members WHERE account = ?',
                (user_id,)
            )
    except sqlite3.Error as e:
        # 處理刪除資料時的錯誤
        print(f"刪除資料時發生錯誤：{str(e)}")

    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    # 將結果以 JSON 格式回傳
    return jsonify(data=result, size=size)

 
@app.route('/getdata', methods=['GET', 'POST'])  # 登入
def getdata():
     

    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    # 將 result 轉換為 JSON 格式並回傳
    return jsonify(data=result, size=size)
 

# 原有的路由處理器保持不變

@app.route('/api/delete_user', methods=['DELETE'])
def delete_user_api():
    # 在這裡從 DELETE 請求中取得要刪除的帳號資訊
    account = request.json.get('account')

    # 在這裡執行刪除操作，刪除資料庫中的資料
    db = get_db()
    try:
        with db:
            db.execute('DELETE FROM members WHERE account = ?', (account,))
    except sqlite3.Error as e:
        # 處理刪除資料時的錯誤
        print(f"刪除資料時發生錯誤：{str(e)}")
        return jsonify(success=False)  # 回傳刪除失敗的回應

    # 取得刪除後的資料
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    # 回傳 JSON 格式的回應，表示刪除成功，並附帶資料和大小
    return jsonify(success=True, data=result, size=size)


@app.route('/api/getdata', methods=['GET'])
def get_data_api():
    # 在這裡獲取資料庫的資料
    # ...

    # 假設取得資料成功，回傳 JSON 格式的資料
    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)
    return jsonify(data=result, size=size)

 

if __name__ == '__main__':
    app.run(debug=True)
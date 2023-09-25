# Blueprint 包裝你的flask(3)
## 前言
話不多說就讓我們開始吧!
[完整code]()
## 架構
```
app/
├── api/
│   ├── __init__.py
│   ├── api.py
│   └── ...
├── auth/
│   ├── __init__.py
│   ├── auth.py
│   └── templates/
│       ├── login.html
│       ├── signup.html
│       └── manager.html
├── backend/
│   ├── __init__.py
│   ├── db.py
│   ├── test.db
│   └── test.sql
├── templates/
│   ├── base.py
│   ├── index.html
├── static/
│   └── css/
│       ├── styles.css
├── view.py
└── app.py
```

解釋：
- `app/` 是頂層目錄，內含各個模組的子目錄和主要應用程式檔案。
- `api/` 目錄存放與 API 相關的程式碼。
  - `__init__.py` 標記 `api/` 為一個 Python 套件。
  - `api.py` 包含 API 相關的路由和視圖函式。
- `auth/` 目錄存放身份驗證相關的程式碼和模板檔案。
  - `__init__.py` 標記 `auth/` 為一個 Python 套件。
  - `auth.py` 包含身份驗證相關的路由和視圖函式。
  - `templates/` 目錄存放身份驗證相關的 HTML 模板檔案。
    - `login.html` 是登入頁面的模板。
    - `signup.html` 是註冊頁面的模板。
    - `manager.html` 是管理者頁面的模板。
- `backend/` 目錄存放與後端資料庫相關的程式碼和資料庫檔案。
  - `__init__.py` 標記 `backend/` 為一個 Python 套件。
  - `db.py` 包含資料庫相關的程式碼，如連接資料庫、執行查詢等。
  - `test.db` 是 SQLite 資料庫檔案。
  - `test.sql` 是用於初始化資料庫的 SQL 檔案。
- `templates/` 目錄存放應用程式共享的 HTML 模板檔案。
  - `base.py` 是基礎模板，可供其他模板繼承。
  - `index.html` 是首頁的模板。
- `static/` 目錄存放靜態檔案，如 CSS、JavaScript 和圖片等。
  - `css/` 目錄存放 CSS 樣式檔案。
    - `styles.css` 是主要的CSS 樣式檔案。
- `view.py` 包含其他視圖函式和路由。
- `app.py` 是應用程式的入口點，用於啟動應用程式。

 

## 範例
由於code有點多今天主要講解`app.py`、`auth資料夾`等
1. auth資料夾
    ```python
    # auth.py
    from flask import Blueprint, render_template, redirect, request,url_for
    from flask_login import login_user, logout_user, current_user,UserMixin,login_required
    from backend.db import get_db
    import sqlite3
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
    ```
    這裡我將之前的註冊、登入、管理者的功能拉出來並以`auth_bp = Blueprint('auth', __name__,template_folder='auth_templates')` 包裝成模組，要注意的事這裡多了`template_folder='auth_templates`這是因為那三個html只有`auth.py`會用到於是我額外拉一個資料夾來放置這三個html，並把這個模組的templates改向為auth_templates，此外html也須做些改。
    ```html
    <!-- login.html -->
    <form action="{{ url_for('auth.login')}}" method="POST">
    <!-- signup.html -->
    <form action="{{ url_for('auth.sign_up')}}" method="POST">
    ```
    原先的url for因為已經不在`app.py`裡面而是一個模組，所以需要透過`auth.`的方式去得到對應fuction。
2. `app.py`
    ```python
    from flask import Flask
    from flask import Flask, g,request,redirect,render_template,url_for,jsonify
    import sqlite3
    from flask_login import LoginManager, UserMixin 

    import secrets
    from backend.db import get_db
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    login_manager = LoginManager()
    login_manager.init_app(app)
    #
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

    from auth.auth import auth_bp
    from views import views_bp
    from api.api import api_blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(api_blueprint)
    if __name__ == '__main__':
        app.run(debug=True)

    ```
    我們把之前flask login拉過來放到`app.py`這是因為每個page都需要用到login state，至於其他功能只要先import再透過`app.register_blueprint()` 將其註冊就好，這樣我們就完成模組化了!

## 總結
學會Blueprint後，會發現在撰寫前就要先想架構，要不然會亂掉，雖然多了一個想架構時間，但是在日後管理上是非常方便的，此外也能更快分工給其他人，也不會有git共編時的conflict，希望大家都能養成用Blueprint的好習慣，至於之後我將帶大家實作在web顯示k線圖。
    

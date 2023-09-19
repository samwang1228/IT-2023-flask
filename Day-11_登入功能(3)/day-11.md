# 登入功能(3) flask login
## 前言
在昨天教導大家如何建立database至於接下來終於來到重頭戲，我將帶大家使用flask login來實現登入功能。
## 介紹
Flask-Login 是 Flask 應用程式中常用的用戶身份驗證和管理套件。它提供了方便的方法來處理用戶登入、登出、保護路由、管理用戶會話等功能。以下是使用 Flask-Login 實現用戶登入的基本步驟：

1. 安裝 Flask-Login：
   開啟終端機，執行以下指令進行安裝：
   ```
   pip install Flask-Login
   ```

2. 初始化 Flask-Login：
   在你的 Flask 應用程式中，導入 `flask_login` 模組並初始化 `LoginManager` 物件，例如：
   ```python
   from flask import Flask
   from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


   app = Flask(__name__)
   login_manager = LoginManager()
   login_manager.init_app(app)
   ```

3. 定義用戶模型（User Model）：
    User 類別繼承自 UserMixin，UserMixin 提供了一些用於處理用戶登入功能的方法和屬性。在這個例子中，User 類別不需要任何額外的內容，所以只有 pass。

    `@login_manager.user_loader 裝飾器`：
    該裝飾器用於註冊用戶加載函式（user_loader），用於從用戶識別符（user_id）加載用戶。在這個例子中，user_loader 函式從資料庫中查詢用戶的密碼，並創建一個 User 物件，將用戶識別符設定為 user_id，最後返回該用戶。

    `@login_manager.request_loader 裝飾器`：
    該裝飾器用於註冊請求加載函式（request_loader），用於從請求中加載用戶。在這個例子中，request_loader 函式從請求表單（request.form）中獲取用戶識別符（user_id），然後從資料庫中查詢用戶的密碼。如果密碼匹配，則創建一個 User 物件，將用戶識別符設定為 user_id，最後返回該用戶。如果密碼不匹配，則返回 None。
   ```python
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
   ```

4. 設定用戶登入視圖：
   實現用戶登入的視圖(endpoint)，接受用戶提供的登入資訊，並進行驗證。驗證成功後，可以使用 `login_user()` 函式將用戶登入。例如：
   ```python
   from flask import request, redirect
   from flask_login import login_user

   @app.route('/login', methods=['POST'])
   def login():
       # 從 POST 請求中獲取用戶名稱和密碼
       username = request.form['username']
       password = request.form['password']

       # 進行用戶驗證，驗證成功時登入用戶
       if verify_user(username, password):
           user = User(username)  # 創建 User 物件，根據自己的需求進行實現
           login_user(user)  # 登入用戶
           return redirect('/dashboard')
       else:
           return 'Invalid username or password'
   ```

5. 設定登出視圖：
   實現用戶登出的視圖(endpoint)，使用 `logout_user()` 函式將用戶登出。例如：
   ```python
   from flask_login import logout_user

   @app.route('/logout')
   def logout():
       logout_user()  # 登出用戶
       return redirect('/login')
   ```

6. 保護路由：
   設定需要用戶驗證的路由，只允許登入的用戶訪問。你可以使用 `@login_required` 裝飾器來標記需要保護的路

由。例如：
   ```python
   from flask_login import login_required

   @app.route('/dashboard')
   @login_required  # 需要用戶登入才能訪問
   def dashboard():
       return 'Welcome to the dashboard'
   ```
## 總結
今天簡單的介紹，讓讀者了解 Flask-Login 功能。至於更詳細的串接將在明天介紹給大家。
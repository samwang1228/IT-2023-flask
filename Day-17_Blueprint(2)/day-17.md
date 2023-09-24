# Blueprint 包裝你的flask(2)
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
由於code有點多今天主要講解`api`、`views.py`、`backend`等
1. backend資料夾
    ```python
    # db.py
    from flask import g 
    import sqlite3
    SQLITE_DB_PATH = 'backend/test.db'
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(SQLITE_DB_PATH)
            # Enable foreign key check
            db.execute("PRAGMA foreign_keys = ON")
        return db
    ```
    許多`.py`都需要與database連線於是我們先包裝成一個package以便之後直接import來用。
2. api資料夾
    ```python
    from flask import Blueprint, jsonify, request

    from backend.db import get_db
    import sqlite3
    api_blueprint = Blueprint('api', __name__)
    SQLITE_DB_PATH='test.db'
    @api_blueprint.route('/api/delete_user', methods=['DELETE'])
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

    @api_blueprint.route('/api/getdata', methods=['GET'])
    def get_data_api():
        # 在這裡獲取資料庫的資料
        # ...

        # 假設取得資料成功，回傳 JSON 格式的資料
        db = get_db()
        result = db.execute('SELECT account, password FROM members').fetchall()
        size = len(result)
        return jsonify(data=result, size=size)
    ```
    我們將之前的刪除user和查看資料的功能額外拉出來，並透過`api_blueprint = Blueprint('api', __name__)`包裝起來

3. `views.py`
    ```python
    from flask import Blueprint, render_template,redirect,url_for
    from flask_login import login_required, current_user
    
    views_bp = Blueprint('views', __name__)

    @views_bp.route('/')
    def index():
        user_id = current_user.get_id()  
        return render_template('index.html', user_id=user_id)
    ```
    用來render與登入認證無關的html，並且用`views_bp = Blueprint('views', __name__)`包裝成模組，之後這裡還會再增加其他page。

 ## 總結
 今天先到這裡，明天繼續模組化。
 

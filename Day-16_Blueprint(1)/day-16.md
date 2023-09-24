# Blueprint 包裝你的flask(1)
## 前言
回顧看昨天的程式發現已經200多行，這樣在管理上會變得很複雜，這也就是flask最大的缺點，然而flask不能像一般python一樣直接寫成module再import，但是flask提供一個方法可以幫助你模組化那就是Blueprint

## 介紹
藍圖（Blueprint）是 Flask 中用於組織和分割應用程式路由和視圖的概念。它可以將相關的路由和視圖函式分組到單獨的模組中，從而實現模組化和可重用性。

使用藍圖可以將應用程式的路由和視圖分成多個模組，每個模組可以專注於特定的功能或子應用程式。這對於組織大型應用程式、將功能模塊化並提高代碼可讀性和可維護性非常有用。

藍圖的主要功能包括：

1. 路由分割：藍圖允許您定義路由和視圖函式，就像在主應用程式中一樣。您可以使用常見的路由裝飾器（如`@route`、`@get`、`@post`等）在藍圖中定義路由。這使得您可以將相關的路由集中在一個地方，提高代碼組織性。

2. 視圖函式分組：藍圖允許您將相關的視圖函式組織在一個模組中。這使得視圖函式的定義更具結構性和可讀性。

3. URL 前綴：您可以在註冊藍圖時指定 URL 前綴。這將自動將所有藍圖中定義的路由添加指定的前綴，從而實現路由的階層結構。

使用藍圖的基本流程如下：

1. 創建藍圖對象：使用 `Blueprint` 類創建一個藍圖對象。您可以指定藍圖的名稱、模組和靜態資源的文件夾。

2. 定義路由和視圖函式：使用路由裝飾器在藍圖中定義路由和視圖函式。

3. 註冊藍圖：在主應用程式中使用 `app.register_blueprint` 方法註冊藍圖。您可以指定 URL 前綴，以及其他選項，如靜態資源 URL 前綴。

這樣，藍圖中定義的路由和視圖函式就可以在應用程式中使用，並根據註冊時的 URL 前

綴進行訪問。

藍圖可以幫助您更好地組織和管理您的 Flask 應用程式，使其具有更好的可擴展性和可維護性。它還提供了一種將應用程式功能模塊化的方法，使您的代碼更易於理解和維護。

## 範例
當您需要使用藍圖來組織和分割 Flask 應用程式的路由和視圖時，下面是一個簡單的示例：

首先，創建一個名為 `auth` 的藍圖，用於處理身份驗證相關的路由和視圖。

```python
# auth.py

from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/register')
def register():
    return render_template('register.html')
```

接下來，在主應用程式中註冊並使用該藍圖：

```python
# app.py

from flask import Flask
from auth import auth_bp

app = Flask(__name__)

# 註冊藍圖
app.register_blueprint(auth_bp, url_prefix='/auth')

# 主應用程式的其他路由和視圖
@app.route('/')
def home():
    return 'Welcome to the home page'

@app.route('/about')
def about():
    return 'About page'

if __name__ == '__main__':
    app.run()
```

在上面的示例中，`auth.py` 文件中定義了一個名為 `auth_bp` 的藍圖，包含了 `/login` 和 `/register` 兩個路由。

然後，在主應用程式 `app.py` 中，使用 `app.register_blueprint` 方法將該藍圖註冊到主應用程式中，並指定 URL 前綴為 `/auth`。這意味著 `/login` 路由將變成 `/auth/login`，`/register` 路由將變成 `/auth/register`。


## 總結
今天介紹了什麼是Blueprint，但是這樣的範例我想大家應該是沒什麼感覺，所以明天我將會把之前的code模組化給大家看。
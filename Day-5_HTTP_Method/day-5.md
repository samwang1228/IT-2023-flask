# HTTP method in flask
## 前言
做天講到Jinja2的相關語法，使讀者能夠將python傳遞給html，那麼今天如果要反過來使html的資料傳遞給python呢?那就要使用HTTP method了，話不多說我們來看看範例吧。
## 範例
當你在 HTML 中使用表單（form）時，你可以指定表單提交時使用的 HTTP 方法。常見的方法有 POST 和 GET。

- POST 方法：當你指定表單的 method 屬性為 "post" 時，表示當用戶提交表單時，將使用 POST 方法將表單數據發送到指定的 URL。POST 方法通常用於向服務器提交敏感或較大的數據，例如用戶名、密碼、文件上傳等。在 Flask 中，你可以使用 `@app.route` 裝飾器指定處理 POST 請求的函數。

```html
<form method="post" action="/submit">
  <!-- 表單內容 -->
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    # 處理 POST 請求的邏輯
    data = request.form.get('data')
    # ...
    return 'Submitted'

if __name__ == '__main__':
    app.run()
```

- GET 方法：當你指定表單的 method 屬性為 "get" 時，表示當用戶提交表單時，將使用 GET 方法將表單數據作為 URL 的一部分發送到指定的 URL。GET 方法通常用於向服務器獲取數據，例如在查詢頁面中提供搜索條件等。在 Flask 中，你可以使用 `@app.route` 裝飾器指定處理 GET 請求的函數。

```html
<form method="get" action="/search">
  <!-- 表單內容 -->
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    # 處理 GET 請求的邏輯
    query = request.args.get('q')
    # ...
    return 'Search results for: ' + query

if __name__ == '__main__':
    app.run()
```
## 總結
表單的 method 屬性與 HTTP 方法（POST、GET 等）的關係在於定義了表單數據提交的方式。根據你的需求和使用情境，可以選擇使用 POST 或 GET 方法來處理表單提交的數據。在 Flask 中，你可以通過指定 `methods` 參數來指定處理不同方法的函數。
至於明天將會教導大家透過指定`methods`來達成上傳檔案的功能。
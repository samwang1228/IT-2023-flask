# 登入功能(1)使用SQLite
## 前言
接下來的三天將會帶大家做登入、註冊、管理者等功能，然而需要這些功能就必須有databasse了，而我們將會使用SQLite實作。
## 介紹
SQLite 是一個輕量級的嵌入式關聯式資料庫管理系統，而 Flask 是一個輕量級的 Python Web 應用框架。在 Flask 中，你可以使用 SQLite 作為資料庫引擎來處理資料持久化和資料庫操作。
## 範例
在 Flask 中使用 SQLite 的步驟如下：

1. 安裝相關套件：確保你已經安裝了 Flask 和 SQLite 庫，你可以使用 pip 套件管理器進行安裝：

   ```
   pip install pysqlite3
   ```

2. 匯入必要的模組：在你的 Flask 應用程式中匯入必要的模組：

   ```python
   from flask import Flask, g
   import sqlite3
   ```

3. 建立sql table 這裡我們創建user、password

   ```sql
   CREATE TABLE members (
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    account TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    );

   ```

4. build db

   ```python
   import sqlite3

    SQLITE_DB_PATH = 'test.db'
    SQLITE_DB_SCHEMA = 'test.sql'

    with open(SQLITE_DB_SCHEMA) as f:
        create_db_sql = f.read()

    db = sqlite3.connect(SQLITE_DB_PATH)

    with db:
        db.executescript(create_db_sql)

    with db:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            'INSERT INTO members (account, password) VALUES ("user", "0000")'
        )

   ```
首先，程式碼中使用 `sqlite3` 模組匯入了 SQLite 庫。

接下來，定義了 SQLite 資料庫的路徑 `SQLITE_DB_PATH`，以及資料庫結構的檔案路徑 `SQLITE_DB_SCHEMA`。

然後，使用 `open` 函式打開資料庫結構的檔案，並讀取其內容，將其存放在 `create_db_sql` 變數中。

接著，使用 `sqlite3.connect` 函式建立與 SQLite 資料庫的連線，並將連線物件存放在 `db` 變數中。

使用 `with db:` 語句開始一個資料庫交易，並使用 `executescript` 方法執行資料庫結構的 SQL 語句，這樣就建立了 `members` 資料表。

接著，再次使用 `with db:` 語句開始一個新的資料庫交易，並執行兩個 SQL 語句。首先，設置 SQLite 的外鍵功能為開啟，這樣就可以使用外鍵約束。然後，執行一個 `INSERT` 語句，將一筆資料插入到 `members` 資料表中。

最後，使用 `with db:` 語句開始一個新的資料庫交易，並執行一個 `CREATE TABLE` 的 SQL 語句，建立了一個 `members` 資料表，該表包含 `id`、`account` 和 `password` 三個欄位。

這個範例中使用了 `with` 語句來確保在操作資料庫時的自動提交和關閉連線。你可以根據需求進行更多的資料庫操作，例如更新資料、刪除資料等。

## 總結
需要注意的是，範例中的 SQL 語句是直接嵌入到程式碼中的，這種方式不夠靈活且不易維護。在實際應用中，建議使用 ORM（物件關聯對映）工具，例如 SQLAlchemy，來管理資料庫模型和執行資料庫操作，不過我們只是要實作簡易的登入功能就不做更深入的探討了，明天將會帶大家串接flask。
 
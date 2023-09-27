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
        'INSERT INTO members (account, password) VALUES ("sam", "0000")'
    )

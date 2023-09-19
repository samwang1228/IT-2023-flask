from flask import Flask, g
import sqlite3
app = Flask(__name__)
app.config['DATABASE'] = 'test.db'
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

@app.route('/create_table')
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    return 'Table created successfully'

@app.route('/insert_data')
def insert_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('John',))
    db.commit()
    return 'Data inserted successfully'

@app.route('/get_data')
def get_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    password = db.execute(
        'SELECT * FROM members'
    ).fetchall()
    return str(password)

if __name__ == '__main__':
    app.run(debug=True)
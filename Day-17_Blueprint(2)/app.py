from flask import Flask
from flask import Flask, g,request,redirect,render_template,url_for,jsonify
import sqlite3
from flask_login import LoginManager, UserMixin 

import secrets
from backend.db import get_db
app = Flask(__name__)
 
app.config['DATABASE'] = 'test.db'
app.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)
SQLITE_DB_PATH = 'test.db'
SQLITE_DB_SCHEMA = 'test.sql'

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

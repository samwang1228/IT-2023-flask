from flask import Blueprint, render_template,redirect,url_for
from flask_login import login_required, current_user
 
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    user_id = current_user.get_id()  
    return render_template('index.html', user_id=user_id)

 
 

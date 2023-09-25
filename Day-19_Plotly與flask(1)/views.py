from flask import Blueprint, render_template,redirect,url_for
from flask_login import login_required, current_user
import plotly.graph_objects as go
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    user_id = current_user.get_id()  
    return render_template('index.html', user_id=user_id)

@views_bp.route('/plot')
@login_required
def plotbar():
    # 建立 Plotly 圖表
    user_id = current_user.get_id()
    fig = go.Figure(data=go.Bar(x=[1, 2, 3], y=[4, 5, 6]))

    # 將圖表轉換為 HTML 字串
    plot_html = fig.to_html()

    # 傳遞圖表 HTML 到模板中
    return render_template('plot.html', plot_html=plot_html,user_id=user_id)
 

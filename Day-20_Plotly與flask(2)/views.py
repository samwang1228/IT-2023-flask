from flask import Blueprint, render_template,redirect,url_for
from flask_login import login_required, current_user
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots
views_bp = Blueprint('views', __name__)
def plot_k_diagram(grouped_data):
    '''
    繪製大盤指數與情緒的疊圖
    grouped_data: 分組後的資料，包含 Open、High、Low、Close 等欄位
    '''
    x_labels = [date.strftime('%m-%d') for date in grouped_data.index]
    increasing_color = 'red'
    decreasing_color = 'green'
    start_date = grouped_data.index.min()
    end_date = grouped_data.index.max()

    # 移除沒有資料的日期
    grouped_data = grouped_data.dropna()

    # 建立子圖表，包含兩個軸
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Candlestick(
            x=grouped_data.index,
            open=grouped_data['Open'],
            high=grouped_data['High'],
            low=grouped_data['Low'],
            close=grouped_data['Close'],
            increasing_line_color=increasing_color,
            decreasing_line_color=decreasing_color,
            name='Stock'
        )
    )

    # 設置圖表的標題和軸標籤
    fig.update_layout(
        width=1000,
        height=600,
        title=dict(
            text='台積電2023年股價',
            font=dict(color='white')
        ),
        xaxis=dict(
            title='時間',
            title_font=dict(color='white'),
            range=[start_date, end_date],  # 設置 x 軸範圍
            type='category',  # 設定 x 軸類型為 category
            tickfont=dict(color='white'),
            ticktext=x_labels,  # 設定刻度標籤文字
            tickvals=list(range(len(x_labels))),  # 設定刻度標籤的索引位置
            showgrid=False,
        ),
        yaxis=dict(
            title='股價',
            title_font=dict(color='white'),
            showgrid=False,
            tickfont=dict(color='white')
        ),
        plot_bgcolor='rgba(0, 0, 0, 0.6)',  # 背景設為透明黑
        paper_bgcolor='rgba(0, 0, 0, 0.7)'  # 背景設為透明
    )

    return fig
@views_bp.route('/')
def index():
    user_id = current_user.get_id()  
    return render_template('index.html', user_id=user_id)

@views_bp.route('/plot')
@login_required
def plotkdiagram():
    # 建立 Plotly 圖表
     
    df = yf.download("2330.TW", start="2023-1-1",end="2023-6-30")
    user_id = current_user.get_id()
     
    fig=plot_k_diagram(df)
    # 將圖表轉換為 HTML 字串
    plot_html = fig.to_html()

    # 傳遞圖表 HTML 到模板中
    return render_template('plot.html', plot_html=plot_html,user_id=user_id)
 

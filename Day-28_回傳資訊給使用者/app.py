 
from flask import Flask, request, abort,render_template
import random,time
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
from urllib.parse import parse_qsl
from func import detect_song,send_response_to_line_bot
#======python的函數庫==========

app = Flask(__name__)
info=[]
with open(os.path.join('..','key.txt'), 'r') as f:
    for line in f:
        info.append(line.strip())
LINE_CHANNEL_SECRET = info[0]
LINE_CHANNEL_ACCESS_TOKEN = info[1]
LIFF_ID = info[2]
LIFF_URL = info[3]
 

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
# 監聽所有來自 /callback 的 Post Request

@app.route('/page')
def page():
    return render_template('index.html', liffid = LIFF_ID)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

 
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    print(mtext)
    
@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
ALLOWED_EXTENSIONS = {'wav','mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  ALLOWED_EXTENSIONS
def get_filename(filename):
    return filename.split('.')[1]
@app.route('/upload', methods=['get'])
def uploads_page():    
     user_id= request.form.get('ID')     
     return render_template('index.html', liffid = LIFF_ID , user_id=user_id)
@app.route('/upload', methods=['POST'])
def upload_file():
    errorMsg=''
    musicname=''
    user_id= request.form.get('ID')
    t=time.time()
    r=random.randrange(0, 101, 2)
    upload_folder = os.path.join("static","upload",user_id,str(t)+str(r))
    file = request.files['filename']    # 取得上傳的檔案 
    if get_filename(file.filename) == 'mp3' or get_filename(file.filename) == 'wav': 
        musicname=file.filename
        # return redirect(url_for('index'))   # 令瀏覽器跳回首頁 
    if file and allowed_file(file.filename):   # 確認有檔案且副檔名在允許之列'
        os.makedirs(upload_folder ,exist_ok=True)
        file.save(os.path.join(upload_folder, file.filename))
    else:
        errorMsg='僅允許上傳mp3、wav音檔'
    detect_song(upload_folder,musicname)
    
    while(1):
        if(os.path.isfile(upload_folder+'/output.txt')):
            break
    send_response_to_line_bot(user_id,'檔案上傳已完成',filedir=os.path.join(upload_folder, 'output.txt'))
    
    return render_template('index.html',errorMsg=errorMsg,filename=file.filename,img_name=musicname,liffid = LIFF_ID,user_id=user_id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port,debug=True)
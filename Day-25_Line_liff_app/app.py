 
from flask import Flask, request, abort,render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
from urllib.parse import parse_qsl
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
    if mtext == '@買pizza':
        message = TemplateSendMessage(
                alt_text='按鈕樣板',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',  #顯示的圖片
                    title='購買PIZZA',  #主標題
                    text='請選擇：',  #副標題
                    actions=[
                        URITemplateAction(  #開啟網頁
                            label='連結網頁',
                            uri=LIFF_URL,
                        ),
                    ]
                )
            )
        
        try:
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

 
@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port,debug=True)
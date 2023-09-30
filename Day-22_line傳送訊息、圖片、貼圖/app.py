 
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
 
 
#======python的函數庫==========

app = Flask(__name__)
 
 
 
LINE_CHANNEL_ACCESS_TOKEN = ''
 
LINE_CHANNEL_SECRET = ''
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
# 監聽所有來自 /callback 的 Post Request
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
    if mtext == '今晚要吃啥':
        try:
            quick_reply_buttons = [
                QuickReplyButton(action=MessageAction(label='Yes', text='Yes!')),
                QuickReplyButton(action=MessageAction(label='No', text='No!')),
            ]
            message = [
                ImageSendMessage(
                original_content_url = "https://i.imgur.com/4QfKuz1.png",
                preview_image_url = "https://i.imgur.com/4QfKuz1.png"
                ), 
            # 建立文字訊息，並加入快速回覆按鈕
                TextSendMessage(
                text='$Do you like this?',
                emojis=
                [
                    {
                        'index': 0, 
                        'productId': '5ac1bfd5040ab15980c9b435', 
                        'emojiId': '008'
                    },
                ],
                quick_reply=QuickReply(items=quick_reply_buttons)
                ),
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
     
        
    elif mtext == 'Yes!':
        try:
            message = StickerSendMessage(  #貼圖兩個id需查表
                package_id='1',  
                sticker_id='2'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

     

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
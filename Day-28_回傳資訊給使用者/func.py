import os
from ShazamAPI import Shazam
from linebot.models import *
from linebot import  LineBotApi, WebhookHandler
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
def detect_song(path,filename):
    output = os.path.join(path,"output.txt")
    fp = open(output,'w')
    print('---------------',path,'--------------------------------')
    print("Files and Directories in '% s':" % path)
    inputfile=os.path.join(path,filename)
    mp3_file_content_to_recognize = open(inputfile, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    t = next(recognize_generator)
    print('song title',t[1]['track']['title'],'\nsinger',t[1]['track']['subtitle'],'\nlyric',t[1]['track']['sections'][1]['text'])
    song_title = 'song title:' + t[1]['track']['title']
    singer = '\nsinger:' + t[1]['track']['subtitle']
    image = '\nimage:' + t[1]['track']['images']['background']
    fp.write(song_title)
    fp.write(singer)
    fp.write(image)
    fp.write('\nlyric:')
    for l in t[1]['track']['sections'][1]['text']:
        fp.write(l)
    fp.close()

def send_response_to_line_bot(user_id, message,filedir):
    ryric=''
    info=[]
    cnt=0
    f = open(filedir,'r')  
    for line in f.readlines():
        cnt+=1
        # print('--------',cnt,'---------')
        if(cnt>=4):
            ryric+=str(line)
        info.append(line)
    # print('--------',ryric)
    # print('--------',info)
    f.close
    picUrl=str(info[2])
    title=str(info[0])
    title=title[11:len(title)-1]
    link=picUrl[6:len(picUrl)-1]
    message = TemplateSendMessage(
        alt_text='按鈕樣板',
        template=ButtonsTemplate(
            thumbnail_image_url=link,  #顯示的圖片
            title=title,  #主標題
            text=info[1],  #副標題
            actions=[
                PostbackTemplateAction(
                            label='查看完整歌詞',
                            data=f'!歌詞{filedir}'
                ),
                    
            ]
        )
    )
    line_bot_api.push_message(user_id, message)

from flask import Flask, render_template,request,flash
import pathlib
import os
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 # 32MB
SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,'static','uploads')
ALLOWED_EXTENSIONS = {'mp4','png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  ALLOWED_EXTENSIONS
def get_filename(filename):
    return filename.split('.')[1]
@app.route('/upload', methods=['get'])
def uploads_page():    
     return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    errorMsg=''
    imgname=''
    file = request.files['filename']    # 取得上傳的檔案 
    if get_filename(file.filename) == 'png' or get_filename(file.filename) == 'jpg': 
        imgname=file.filename
        # return redirect(url_for('index'))   # 令瀏覽器跳回首頁 
    if file and allowed_file(file.filename):   # 確認有檔案且副檔名在允許之列'
        os.makedirs(UPLOAD_FOLDER ,exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    else:
        errorMsg='僅允許上傳mp4、mov影像檔'
    return render_template('upload.html',errorMsg=errorMsg,filename=file.filename,img_name=imgname)
@app.errorhandler(413)
def request_entity_too_large(error):
    # 自訂錯誤處理邏輯
    errorMsg='僅允許上傳32MB以下的檔案'    
    return render_template('error.html',errorMsg=errorMsg), 413
@app.errorhandler(404)
def page_not_found(error):
    # 自訂錯誤處理邏輯
    errorMsg='此頁面不存在!'   
    return render_template('error.html',errorMsg=errorMsg), 404
if __name__ == '__main__':
    app.run(debug=True)
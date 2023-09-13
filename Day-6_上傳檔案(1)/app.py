from flask import Flask, request,render_template
import os
app = Flask(__name__)
@app.route('/upload', methods=['get'])
def upload_page():
    return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['filename']  # 獲取上傳的文件
    file.save(os.path.join(file.filename))
    # 在這裡處理上傳的文件，例如保存到本地或進行其他處理

    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)
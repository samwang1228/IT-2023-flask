# 上傳檔案(1)
## 前言
在昨天的範例中我們已經學會使用form、post來達成html與flask的溝通，而常見的上傳檔案也是透過此方法，接下兩天帶大家來操作。
[完整code在這裡]()
## 範例
在 Flask 中，你可以輕鬆實現文件上傳功能。以下是一個簡單的步驟和代碼示例：

1. 在 `Day-3的HTML` 中添加此程式：
```html
 <form method="POST" enctype="multipart/form-data" action="{{ url_for('upload_file') }}">
             <input type="file" id="getFile"  name="filename" required>
            <input type="submit" class="btn btn-outline-info" value="上傳" >
</form>
```

注意 `enctype="multipart/form-data"` 是必需的，它指定表單的編碼類型，以支持文件上傳。

2. 在 Flask 應用中添加路由處理函數來處理文件上傳：
```python
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
```

在上面的例子中，我們使用`get`來顯示web page，以及使用`post`和 `request.files` 來獲取上傳的文件，其中 `'filename'` 是文件上傳字段的名稱，與 HTML 表單中的 `name="filename"` 對應，接者再透過`file.save(os.path.join(file.filename))`來儲存至指定位置其中`flie.filename`為使用者原本的檔案名稱
需要注意的是，Flask 預設只允許上傳特定類型的文件（例如圖像、文檔等），並對文件大小進行了限制。你可以在 Flask 應用中配置這些限制，以及其他文件上傳相關的設置。
## 結果
![web](test.png)
![dir](1.png)
## 總結
這只是一個簡單的文件上傳示例，你可以根據實際需求進行更複雜的文件處理和驗證。Flask 提供了強大而靈活的功能來處理文件上傳，讓你可以輕鬆實現各種文件相關的應用，明天我將會帶大家使用更進階的應用。
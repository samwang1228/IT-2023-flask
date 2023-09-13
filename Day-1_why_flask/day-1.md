# day-1 why flask?
## 介紹
常見的python後端有flask、django那麼為什麼我選擇flask當作本次的IT賽呢? 在下方提供範例與比較供讀者參考
## 比較

|  | django | flask |
| -------- | -------- | -------- |
| 系統     | 內建功能較完整，像是提供了管理面板，數據庫界面，目錄結構和ORM的全方位體驗     | 需要透過第三方套件去擴充 |
|  適用    | 適合大型系統ex 校務網站、購物車     |適合小型系統ex chat bot、在線社交網絡|
|  資安    | 較安全     |較不安全因使用第三方套件|
|  靈活性    | 較低     |較高(寫法不會那固麼定)|
|  效能   | 較差     |較快|
|  學習成本    | 較高     |較低|
|  使用範例    | Instagram、Spotify     |LinkedIn，Netflix|

僅透過別人的建議來評估是不好的，因此以下提供實際範例供讀者參考
## django
### 創建 django 專案
```python!
pip install Django
cd "你要的django 專案資料夾"
django-admin startproject "你自訂義的專案名稱"
cd "你自訂義的專案名稱"
python manage.py runserver #會創建一個http://127.0.0.1:8000/的網站
python manage.py migrate # 如果有更新到模組
```
![](https://hackmd.io/_uploads/B1YwSRHI2.png)
* manage.py:管理程式的窗口
* settings.py: 整個專案的設定工作
* urls.py: 網址對應工作，可定義伺服器收到什麼網址後，要把工作交給哪一* 個函數處理
* wsgi.py: 部屬到主機時才用的到
* init.py: 代表文件夾下的東西可以被其他東西引入

### 綁定html
* 要在有manage.py的路徑下新增templates資料夾此資料夾可放入已寫好的html
![](https://hackmd.io/_uploads/SJWHFmL8h.png)
* 在urls.py新增網址並對應views.py的函式
```python!
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', view.login_view, name='login'),
]
```
* 在views.py裡增加功能
```python
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 檢驗登入 先以假的當作範例
        if username=='test' and password=='0000': 
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # 要用字典的方式傳給html
        hello_py='hello'
        return render(request, 'login.html',{"hello":hello_py})
```
### 插入css、js、img
* html
``` html
# 要先在要使用的html頂端插入下面
{% load static %}
# 使用方法
<link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}">
<script src="{% static 'js/scripts.js' %}"type="text/javascript"></script>
```
* setting.py
```python!
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,  'statics'),
]
```

## flask
### 創建flask專案
```python!
pip install flask
# 手動新增app.py並加上以下幾行code
from flask import Flask
app = Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()
# 啟動app.py
python app.py
#會創建一個http://127.0.0.1:5000/的網站
```
### 綁定html
* 在有app.py的目錄下創建templates、static資料夾
![](https://hackmd.io/_uploads/S1RPijtUh.png)
* 增網址並對應函式
```python
@app.route('/register', methods=['GET', 'POST']) #綁定網址
def login():
    if request.method == 'POST':
        # 取得html form的資料
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 檢驗登入 先以假的當作範例
        if username=='test' and password=='0000': 
            login_user(user)
            return redirect( url_for('index') )
        else:
            error_message = 'Invalid username or password.'
            return render_template('login.html', error_message=error_message)
    else:
        # 將python變數傳給html
        hello_py='hello'
        return render('login.html',hello_py=hello_py)
```
### 插入css、js、img
```html
<link type="text/css"href="{{ url_for('static', filename='css/styles.css') }}"/>
<script src="{{ url_for('static', filename='js/scripts.js') }}" type="text/javascript">            
<img src="{{ url_for('static', filename='images/img/qrcode.jpg') }}" width="200px" height="200px">

```
## 總結
從範例中應該不難看出，flask如果今天要做大型專案app.py會變得很長不好管理，但是在撰寫上是相當簡潔的，且flask提供了Blueprint來達成模組化，所以用模組化的方式去撰寫就能間得雙方優點。
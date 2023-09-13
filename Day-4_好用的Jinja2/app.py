# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    username = 'John'
    items = ['Apple', 'Banana', 'Orange']
    date = '2022-01-01'
    return render_template('index.html', username=username, date=date, items=items)

if __name__ == '__main__':
    app.run(debug=True)
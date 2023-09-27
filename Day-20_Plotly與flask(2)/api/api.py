from flask import Blueprint, jsonify, request

from backend.db import get_db
import sqlite3
api_blueprint = Blueprint('api', __name__)
SQLITE_DB_PATH='test.db'
@api_blueprint.route('/api/delete_user', methods=['DELETE'])
def delete_user_api():
    # 在這裡從 DELETE 請求中取得要刪除的帳號資訊
    account = request.json.get('account')

    # 在這裡執行刪除操作，刪除資料庫中的資料
    db = get_db()
    try:
        with db:
            db.execute('DELETE FROM members WHERE account = ?', (account,))
    except sqlite3.Error as e:
        # 處理刪除資料時的錯誤
        print(f"刪除資料時發生錯誤：{str(e)}")
        return jsonify(success=False)  # 回傳刪除失敗的回應

    # 取得刪除後的資料
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)

    # 回傳 JSON 格式的回應，表示刪除成功，並附帶資料和大小
    return jsonify(success=True, data=result, size=size)

@api_blueprint.route('/api/getdata', methods=['GET'])
def get_data_api():
    # 在這裡獲取資料庫的資料
    # ...

    # 假設取得資料成功，回傳 JSON 格式的資料
    db = get_db()
    result = db.execute('SELECT account, password FROM members').fetchall()
    size = len(result)
    return jsonify(data=result, size=size)
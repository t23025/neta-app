# db作成後、編集を書けたりアプリと連動させるときに必要。
# 必要なモジュールをインポート
from fastapi import FastAPI, HTTPException  # FastAPIの基本機能とHTTPエラー処理
from fastapi.responses import JSONResponse  # JSONレスポンスとして返すため
from pydantic import BaseModel              # 入力データのバリデーションと型チェック
import sqlite3                              # 組み込みのSQLiteライブラリでDB操作
# FastAPIアプリケーションを初期化
app = FastAPI()

# データベースファイルのパスとテーブル名
DB_NAME = "C:/Users/T23025/Desktop/まとめ/neta-app/app/api/neta.db" # SQLiteのDBファイルのパス
TABLE_NAME = "my_table"  # 使用するテーブル名

# データベース初期化関数（テーブルがなければ作成）
def init_db():
    connection = sqlite3.connect(DB_NAME)  # データベースへ接続
    cursor = connection.cursor()# SQL操作のためのカーソルを作成
    # テーブルを作成（なければ）
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date INTEGER,
        place TEXT,
        time INTEGER,
        kaga TEXT,
        kaya TEXT,
        dialect TEXT,
        url TEXT,
        count INTEGER
    )
    """)
    connection.commit()  # テーブル作成の変更を保存
    connection.close()  # DB接続を閉じる

# Pydanticモデル：POST/PUT時のデータ形式を定義
class Item(BaseModel):  # クライアントから受け取るデータの構造を定義するモデル
    title: str           # タイトル（必須）
    date: int = 0        # 日付（任意、初期値0）
    place: str           # 場所（必須）
    time: int = 0        # 時間（任意、初期値0）
    kaga: str            # 加賀側の出演者や内容
    kaya: str            # 加屋側の出演者や内容
    dialect: str         # 方言や話し方の特徴
    url: str             # 関連するURL（YouTubeなど）
    count: int = 0       # カウント（再生数など、初期値0）
# データベースに接続する補助関数
def get_db_connection():  # データベースへの接続を行う補助関数
    return sqlite3.connect(DB_NAME)  # DBに接続して返す
# 全データを取得（GET /items）
@app.get("/items")  # 全てのアイテムを取得するGETエンドポイント
def get_items():
    connection = get_db_connection()  # DB接続を取得
    cursor = connection.cursor()  # カーソル作成
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")  # 全ての行を取得するSQLを実行
    rows = cursor.fetchall()  # 結果をすべて取得
    connection.close()  # DB接続を閉じる
    return JSONResponse(content=[{  # 各行を辞書にしてJSONとして返す
        "id": row[0],
        "title": row[1],
        "date": row[2],
        "place": row[3],
        "time": row[4],
        "kaga": row[5],
        "kaya": row[6],
        "dialect": row[7],
        "url": row[8],
        "count": row[9]
    } for row in rows])

# 再生数順にデータ取得（GET /items/by_count）
@app.get("/items/by_count")  # カウント順（再生数など）で並べ替えて取得するエンドポイント
def get_items_by_count():
    connection = get_db_connection()  # DBへ接続
    cursor = connection.cursor()  # カーソルを作成
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY count DESC")  # countを降順で取得
    rows = cursor.fetchall()  # 全件取得
    connection.close()  # 接続を閉じる
    return JSONResponse(content=[{  # 結果を整形してJSONとして返す
        "id": row[0], "title": row[1], "date": row[2], "place": row[3],
        "time": row[4], "kaga": row[5], "kaya": row[6], "dialect": row[7],
        "url": row[8], "count": row[9]
    } for row in rows])

# フィルターで取得（GET /items/filter?min_count=〇&from_date=〇〇〇〇）
@app.get("/items/filter")  # フィルター付きでデータを取得するGETエンドポイント
def filter_items(min_count: int = 0, from_date: str = "0000-01-01"):  # クエリパラメータでcountと日付を指定
    connection = get_db_connection()  # DBに接続
    cursor = connection.cursor()  # カーソル作成
    # 指定されたcount以上、日付以降のデータを取得
    cursor.execute(f"""
        SELECT * FROM {TABLE_NAME}
        WHERE count >= ? AND date >= ?
        ORDER BY date DESC
    """, (min_count, from_date))
    rows = cursor.fetchall()  # 結果を取得
    connection.close()  # 接続を閉じる
    return JSONResponse(content=[{  # 結果をJSON形式で返す
        "id": row[0], "title": row[1], "date": row[2], "place": row[3],
        "time": row[4], "kaga": row[5], "kaya": row[6], "dialect": row[7],
        "url": row[8], "count": row[9]
    } for row in rows])

# データを追加（POST /items）
@app.post("/items")  # 新しいアイテムを作成するPOSTエンドポイント
def create_item(item: Item):  # リクエストボディとしてItemを受け取る
    connection = get_db_connection()  # DB接続
    cursor = connection.cursor()  # カーソル作成
    cursor.execute(  # INSERT文でデータを追加
        f"INSERT INTO {TABLE_NAME} (title, date, place, time, kaga, kaya, dialect, url, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (item.title, item.date, item.place, item.time, item.kaga, item.kaya, item.dialect, item.url, item.count),
    )
    connection.commit()  # 変更を保存
    item_id = cursor.lastrowid  # 追加されたデータのIDを取得
    connection.close()  # 接続を閉じる
    return JSONResponse(content={  # 作成されたアイテムのデータを返す
        "id": item_id, 
        "title": item.title, 
        "date": item.date, 
        "place": item.place, 
        "time": item.time, 
        "kaga": item.kaga,
        "kaya": item.kaya,
        "dialect": item.dialect,
        "url": item.url,
        "count": item.count
    })
# データを削除（DELETE /items/{item_id}）
@app.delete("/items/{item_id}")  # アイテムを削除するDELETEエンドポイント
def delete_item(item_id: int):  # URLパスでIDを受け取る
    connection = get_db_connection()  # DB接続
    cursor = connection.cursor()  # カーソル作成
    # IDに該当するデータが存在するか確認
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (item_id,))  # 指定IDの存在確認
    row = cursor.fetchone()  # 結果取得
    if row is None:  # データが存在しない場合
        connection.close()  # 接続を閉じて
        raise HTTPException(status_code=404, detail="Item not found")  # 404エラーを返す
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (item_id,))  # 削除実行
    connection.commit()  # 変更保存
    connection.close()  # 接続を閉じる
    return JSONResponse(content={"message": "Item deleted successfully"})  # 削除成功メッセージを返す
# データを更新（PATCH /items/{item_id}）
@app.patch("/items/{item_id}")  # アイテムを更新するPATCHエンドポイント
def update_item(item_id: int, item: Item):  # URLパスとリクエストボディで更新データを受け取る
    connection = get_db_connection()  # DB接続
    cursor = connection.cursor()  # カーソル作成
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (item_id,))  # 対象IDの確認
    row = cursor.fetchone()  # 結果取得
    if row is None:  # データがなければ
        connection.close()  # 接続を閉じて
        raise HTTPException(status_code=404, detail="Item not found")  # 404エラーを返す
    cursor.execute(  # データを更新
        f"UPDATE {TABLE_NAME} SET title = ?, date = ?, place = ?, time = ?, kaga = ?, kaya = ?, dialect = ?, url = ?, count = ?  WHERE id = ?",
        (item.title, item.date, item.place, item.time, item.kaga, item.kaya, item.dialect, item.url, item.count, item_id),
    )
    connection.commit()  # 変更を保存
    connection.close()  # 接続を閉じる
    return JSONResponse(content={  # 更新後のデータを返す
        "id": item_id, 
        "title": item.title, 
        "date": item.date, 
        "place": item.place, 
        "time": item.time, 
        "kaga": item.kaga,
        "kaya": item.kaya,
        "dialect": item.dialect,
        "url": item.url,
        "count": item.count
    })

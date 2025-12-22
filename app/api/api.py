import sqlite3  # SQLiteデータベースとの接続に使用
from fastapi import FastAPI  # FastAPIフレームワーク本体
from pydantic import BaseModel  # リクエストボディのバリデーションと構造定義に使用
from fastapi.middleware.cors import CORSMiddleware  # CORS（クロスオリジン）設定のためのミドルウェア
from fastapi.responses import JSONResponse  # JSON形式のHTTPレスポンスを返すためのクラス
from typing import Optional  # 任意の（Noneを許容する）型を定義するために使用
import calendar  # 月末日など日付関連の計算に使用

# リクエストボディのモデル定義（入力パラメータをまとめたクラス）
class Item(BaseModel):
    query1: Optional[str] = None  # タイトル検索用キーワード
    query2: Optional[str] = None  # 場所検索用キーワード
    startYear: Optional[str] = None  # 開始年
    startMonth: Optional[str] = None  # 開始月
    endYear: Optional[str] = None  # 終了年
    endMonth: Optional[str] = None  # 終了月
    durationMin: Optional[int] = None  # 最小時間（分）
    durationMax: Optional[int] = None  # 最大時間（分）
    dialect: Optional[str] = None  # 方言
    kaga: Optional[str] = None  # 加賀
    kaya: Optional[str] = None  # 賀屋

# FastAPIアプリケーションのインスタンス作成
app = FastAPI()

# CORS 許可設定（React などからアクセスするため）セキュリティのやつ　忘れるな
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 許可するフロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可　なんで["*"]なのか理由を述べられるように
    allow_headers=["*"],  # 全てのヘッダーを許可
)

# 秒 → 分:秒 に変換する関数
def seconds_to_mmss(seconds):
    if seconds is None:
        return None
    minutes = seconds // 60  # 分を計算　//割り算の商
    sec = seconds % 60  # 残りの秒を計算　%割り算のあまり
    return f"{minutes}:{sec:02}"  # フォーマットして返す

# 検索API　 /search エンドポイント（POST）: データベースを検索して結果を返す
@app.post("/search")
def select(item: Item):
    with sqlite3.connect('neta.db') as conn:  # SQLiteデータベースへ接続
        sql = "SELECT * FROM my_table WHERE 1=1"  # ベースとなるSQL文
        data = []  # プレースホルダの値を格納するリスト

        # タイトル検索が指定された場合
        if item.query1 is not None:
            sql += " AND title LIKE ?"  # タイトルに部分一致
            data.append(f"%{item.query1}%")  # プレースホルダに値を追加

        # 場所検索が指定された場合
        if item.query2 is not None:
            sql += " AND place LIKE ?"  # 場所に部分一致
            data.append(f"%{item.query2}%")

        # 最小時間（分）が指定された場合
        if item.durationMin is not None:
            sql += " AND time >= ?"  # 秒数に変換して比較
            data.append(item.durationMin * 60)

        # 最大時間（分）が指定された場合
        if item.durationMax is not None:
            sql += " AND time <= ?"
            data.append(item.durationMax * 60)

        # 方言が指定された場合
        if item.dialect:
            sql += " AND dialect = ?"
            data.append(item.dialect)

        # 加賀フィールドが指定された場合
        if item.kaga:
            sql += " AND kaga LIKE ?"
            data.append(f"%{item.kaga}%")

        # 茅フィールドが指定された場合
        if item.kaya:
            sql += " AND kaya LIKE ?"
            data.append(f"%{item.kaya}%")

        # startYearだけでも指定あればstart_dateを決定
        if item.startYear and item.startYear != "none":
            try:
                start_month = item.startMonth if (item.startMonth and item.startMonth != "none") else "01"
                start_date = int(f"{item.startYear}{str(start_month).zfill(2)}01")  # YYYYMMDD形式に変換
                sql += " AND date >= ?"
                data.append(start_date)
            except Exception as e:
                print(f"start date parse error: {e}") # エラーログ出力

        # endYearだけでも指定あればend_dateを決定
        if item.endYear and item.endYear != "none":
            try:
                if item.endMonth and item.endMonth != "none":
                    # 月が指定されていればその月の末日を取得
                    last_day = calendar.monthrange(int(item.endYear), int(item.endMonth))[1]
                    end_day = str(last_day).zfill(2)
                    end_month = str(item.endMonth).zfill(2)
                else:
                    # 月が未指定なら12月31日とする
                    end_month = "12"
                    end_day = "31"
                end_date = int(f"{item.endYear}{end_month}{end_day}")  # YYYYMMDD形式
                sql += " AND date <= ?"
                data.append(end_date)
            except Exception as e:
                print(f"end date parse error: {e}")  # エラーログ出力

        # 実行するSQLとパラメータをログ出力（デバッグ用）
        print("SQL:", sql)
        print("Params:", data)

        # SQLを実行し、結果を取得
        cursor = conn.execute(sql, data)
        rows = cursor.fetchall()

        # 結果を辞書形式に整形してリストに格納
        dic_list = []
        for row in rows:
            dic = {
                "id": row[0],
                "title": row[1],
                "date": f"{str(row[2])[:4]}-{str(row[2])[4:6]}-{str(row[2])[6:]}",  # YYYYMMDD → YYYY-MM-DD に変換
                "place": row[3],
                "time": seconds_to_mmss(row[4]),  # 秒数を分:秒に変換
                "kaga": row[5],
                "kaya": row[6],
                "dialect": row[7],
                "url": row[8],
                "count": row[9]
            }
            dic_list.append(dic)

        # JSON形式でレスポンスを返す
        return JSONResponse(content=dic_list)

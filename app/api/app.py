import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import calendar

# リクエストボディのモデル
class Item(BaseModel):
    query1: Optional[str] = None
    query2: Optional[str] = None
    startYear: Optional[str] = None
    startMonth: Optional[str] = None
    endYear: Optional[str] = None
    endMonth: Optional[str] = None
    durationMin: Optional[int] = None
    durationMax: Optional[int] = None
    dialect: Optional[str] = None
    kaga: Optional[str] = None
    kaya: Optional[str] = None



app = FastAPI()

# CORS 許可設定（React などからアクセスするため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 秒 → 分:秒 に変換する関数
def seconds_to_mmss(seconds):
    if seconds is None:
        return None
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02}"

# 検索API
@app.post("/search")
def select(item: Item):
    with sqlite3.connect('neta.db') as conn:
        sql = "SELECT * FROM my_table WHERE 1=1"
        data = []
        # タイトル検索
        if item.query1 is not None:
            sql += " AND title LIKE ?"
            data.append(f"%{item.query1}%")

        # 場所検索
        if item.query2 is not None:
            sql += " AND place LIKE ?"
            data.append(f"%{item.query2}%")

        if item.durationMin is not None:
            sql += " AND time >= ?"
            data.append(item.durationMin * 60)

        if item.durationMax is not None:
            sql += " AND time <= ?"
            data.append(item.durationMax * 60)

        if item.dialect:
            sql += " AND dialect = ?"
            data.append(item.dialect)

        if item.kaga:
            sql += " AND kaga LIKE ?"
            data.append(f"%{item.kaga}%")

        if item.kaya:
            sql += " AND kaya LIKE ?"
            data.append(f"%{item.kaya}%")

        # startYearだけでも指定あればstart_dateを決定
        if item.startYear and item.startYear != "none":
            try:
                start_month = item.startMonth if (item.startMonth and item.startMonth != "none") else "01"
                start_date = int(f"{item.startYear}{str(start_month).zfill(2)}01")
                sql += " AND date >= ?"
                data.append(start_date)
            except Exception as e:
                print(f"start date parse error: {e}")

        # endYearだけでも指定あればend_dateを決定
        if item.endYear and item.endYear != "none":
            try:
                if item.endMonth and item.endMonth != "none":
                    last_day = calendar.monthrange(int(item.endYear), int(item.endMonth))[1]
                    end_day = str(last_day).zfill(2)
                    end_month = str(item.endMonth).zfill(2)
                else:
                    # endMonthが指定ないなら12月末日を使う
                    end_month = "12"
                    end_day = "31"
                end_date = int(f"{item.endYear}{end_month}{end_day}")
                sql += " AND date <= ?"
                data.append(end_date)
            except Exception as e:
                print(f"end date parse error: {e}")




        print("SQL:", sql)
        print("Params:", data)

        cursor = conn.execute(sql, data)
        rows = cursor.fetchall()

        dic_list = []
        for row in rows:
            dic = {
                "id": row[0],
                "title": row[1],
                "date": f"{str(row[2])[:4]}-{str(row[2])[4:6]}-{str(row[2])[6:]}",
                "place": row[3],
                "time": seconds_to_mmss(row[4]),
                "kaga": row[5],
                "kaya": row[6],
                "dialect": row[7],
                "url": row[8],
                "count": row[9]
            }
            dic_list.append(dic)


        return JSONResponse(content=dic_list)

import sqlite3
import calendar
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# =========================
# FastAPI app
# =========================
app = FastAPI()

# CORS（本番は必要に応じて絞る）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # とりあえず全部許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DB 初期化
# =========================
DB_NAME = "neta.db"
TABLE_NAME = "my_table"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

init_db()

# =========================
# Models
# =========================
class SearchItem(BaseModel):
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


class Item(BaseModel):
    title: str
    date: int
    place: str
    time: int
    kaga: str
    kaya: str
    dialect: str
    url: str
    count: int = 0

# =========================
# Utils
# =========================
def seconds_to_mmss(seconds: Optional[int]):
    if seconds is None:
        return None
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02}"

def get_db():
    return sqlite3.connect(DB_NAME)

# =========================
# Health check
# =========================
@app.get("/")
def root():
    return {"status": "ok"}

# =========================
# Search API（フロント用）
# =========================
@app.post("/search")
def search(item: SearchItem):
    conn = get_db()
    cursor = conn.cursor()

    sql = f"SELECT * FROM {TABLE_NAME} WHERE 1=1"
    params = []

    if item.query1:
        sql += " AND title LIKE ?"
        params.append(f"%{item.query1}%")

    if item.query2:
        sql += " AND place LIKE ?"
        params.append(f"%{item.query2}%")

    if item.durationMin is not None:
        sql += " AND time >= ?"
        params.append(item.durationMin * 60)

    if item.durationMax is not None:
        sql += " AND time <= ?"
        params.append(item.durationMax * 60)

    if item.dialect:
        sql += " AND dialect = ?"
        params.append(item.dialect)

    if item.kaga:
        sql += " AND kaga LIKE ?"
        params.append(f"%{item.kaga}%")

    if item.kaya:
        sql += " AND kaya LIKE ?"
        params.append(f"%{item.kaya}%")

    if item.startYear and item.startYear != "none":
        start_month = item.startMonth if item.startMonth and item.startMonth != "none" else "01"
        start_date = int(f"{item.startYear}{str(start_month).zfill(2)}01")
        sql += " AND date >= ?"
        params.append(start_date)

    if item.endYear and item.endYear != "none":
        if item.endMonth and item.endMonth != "none":
            last_day = calendar.monthrange(int(item.endYear), int(item.endMonth))[1]
            end_date = int(f"{item.endYear}{str(item.endMonth).zfill(2)}{str(last_day).zfill(2)}")
        else:
            end_date = int(f"{item.endYear}1231")
        sql += " AND date <= ?"
        params.append(end_date)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "title": row[1],
            "date": f"{str(row[2])[:4]}-{str(row[2])[4:6]}-{str(row[2])[6:]}",
            "place": row[3],
            "time": seconds_to_mmss(row[4]),
            "kaga": row[5],
            "kaya": row[6],
            "dialect": row[7],
            "url": row[8],
            "count": row[9],
        })

    return JSONResponse(content=result)

# =========================
# CRUD API（管理用）
# =========================
@app.get("/items")
def get_items():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    conn.close()

    return JSONResponse(content=[
        {
            "id": r[0],
            "title": r[1],
            "date": r[2],
            "place": r[3],
            "time": r[4],
            "kaga": r[5],
            "kaya": r[6],
            "dialect": r[7],
            "url": r[8],
            "count": r[9],
        }
        for r in rows
    ])

@app.post("/items")
def create_item(item: Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        INSERT INTO {TABLE_NAME}
        (title, date, place, time, kaga, kaya, dialect, url, count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item.title,
            item.date,
            item.place,
            item.time,
            item.kaga,
            item.kaya,
            item.dialect,
            item.url,
            item.count,
        )
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return {"id": item_id, **item.dict()}

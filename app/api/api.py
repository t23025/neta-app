# db作成後、編集を書けたりアプリと連動させるときに必要。
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
# Define FastAPI app
app = FastAPI()
# Define database and table
DB_NAME = "C:/Users/T23025/Desktop/まとめ/neta-app/app/api/neta.db"
TABLE_NAME = "my_table"
def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
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
    connection.commit()
    connection.close()

# Define Pydantic model
class Item(BaseModel):
    title: str
    date: int = 0
    place: str
    time: int = 0
    kaga: str
    kaya: str
    dialect: str
    url: str
    count: int = 0
# Helper function to connect to the database
def get_db_connection():
    return sqlite3.connect(DB_NAME)
# Routes
@app.get("/items")
def get_items():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    connection.close()
    return JSONResponse(content=[{
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

@app.get("/items/by_count")
def get_items_by_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY count DESC")
    rows = cursor.fetchall()
    connection.close()
    return JSONResponse(content=[{
        "id": row[0], "title": row[1], "date": row[2], "place": row[3],
        "time": row[4], "kaga": row[5], "kaya": row[6], "dialect": row[7],
        "url": row[8], "count": row[9]
    } for row in rows])

@app.get("/items/filter")
def filter_items(min_count: int = 0, from_date: str = "0000-01-01"):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM {TABLE_NAME}
        WHERE count >= ? AND date >= ?
        ORDER BY date DESC
    """, (min_count, from_date))
    rows = cursor.fetchall()
    connection.close()
    return JSONResponse(content=[{
        "id": row[0], "title": row[1], "date": row[2], "place": row[3],
        "time": row[4], "kaga": row[5], "kaya": row[6], "dialect": row[7],
        "url": row[8], "count": row[9]
    } for row in rows])


@app.post("/items")
def create_item(item: Item):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} (title, date, place, time, kaga, kaya, dialect, url, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (item.title, item.date, item.place, item.time, item.kaga, item.kaya, item.dialect, item.url, item.count),
    )
    connection.commit()
    item_id = cursor.lastrowid
    connection.close()
    return JSONResponse(content={
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
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if row is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Item not found")
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Item deleted successfully"})
@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if row is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Item not found")
    cursor.execute(
        f"UPDATE {TABLE_NAME} SET title = ?, date = ?, place = ?, time = ?, kaga = ?, kaya = ?, dialect = ?, url = ?, count = ?  WHERE id = ?",
        (item.title, item.date, item.place, item.time, item.kaga, item.kaya, item.dialect, item.url, item.count, item_id),
    )
    connection.commit()
    connection.close()
    return JSONResponse(content={
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

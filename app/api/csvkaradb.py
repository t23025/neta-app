import sqlite3
import csv

def time_to_seconds(tstr):
    try:
        minutes, seconds = map(int, tstr.split(":"))
        return minutes * 60 + seconds
    except:
        return None

def date_to_int(dstr):
    try:
        # '2021-07-02' -> 20210702
        return int(dstr.replace("-", ""))
    except:
        return None

db_name = 'neta.db'
csv_name = 'neta.csv'

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS my_table")

cursor.execute('''
    CREATE TABLE my_table(
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
''')

with open('C:/Users/T23025/Desktop/まとめ/neta-app/app/api/neta.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        try:
            date_int = date_to_int(row[1])
            time_sec = time_to_seconds(row[3])
            cursor.execute('''
                INSERT INTO my_table (title, date, place, time, kaga, kaya, dialect, url, count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row[0], date_int, row[2], time_sec,
                row[4], row[5], row[6], row[7], int(row[8])
            ))
        except ValueError:
            print(f"Invalid data in row: {row}")
        except Exception as e:
            print(f"Error inserting row {row}: {e}")
    conn.commit()

cursor.execute("SELECT * FROM my_table")
rows = cursor.fetchall()
print("ROWS", rows)
for row in rows:
    print(row)

conn.close()

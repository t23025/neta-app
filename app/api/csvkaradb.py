import sqlite3  # SQLite データベース操作用の標準ライブラリ
import csv      # CSVファイルの読み取りに使用

# 文字列の「分:秒」を「秒数」に変換する関数
def time_to_seconds(tstr):
    try:
        minutes, seconds = map(int, tstr.split(":"))  # 文字列を「:」で分割し整数化
        return minutes * 60 + seconds  # 分→秒換算して合計
    except:
        return None  # エラー（変換できない形式など）の場合は None を返す

# 日付（YYYY-MM-DD）を整数（YYYYMMDD）に変換する関数
def date_to_int(dstr):
    try:
        return int(dstr.replace("-", ""))  # 「-」を削除して整数化
    except:
        return None  # エラー時は None

# SQLite データベース名
db_name = 'neta.db'
# CSV ファイル名
csv_name = 'neta.csv'

# SQLite データベースに接続
conn = sqlite3.connect(db_name)
# カーソルオブジェクトを作成（SQL文を実行するため）
cursor = conn.cursor()

# 既存のテーブルがあれば削除（初期化）v
cursor.execute("DROP TABLE IF EXISTS my_table")

# 新たにテーブル作成
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

# CSV ファイルを開いて読み込む（エンコーディングはUTF-8）
with open('C:/Users/T23025/Desktop/まとめ/neta-app/app/api/neta.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)  # CSVリーダーを作成
    next(reader, None)         # ヘッダー行をスキップ
    # 各行を1件ずつ処理
    for row in reader:
        try:
            date_int = date_to_int(row[1])  # 日付文字列 → 整数（YYYYMMDD）
            time_sec = time_to_seconds(row[3])  # ネタ時間「分:秒」→ 秒
            # INSERT クエリを実行（プレースホルダ付き）
            cursor.execute('''
                INSERT INTO my_table (title, date, place, time, kaga, kaya, dialect, url, count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row[0], date_int, row[2], time_sec,
                row[4], row[5], row[6], row[7], int(row[8])
            ))
        except ValueError:
            print(f"Invalid data in row: {row}")  # 変換できないデータがあった場合
        except Exception as e:
            print(f"Error inserting row {row}: {e}")  # その他エラーの詳細を出力
    conn.commit()  # すべての変更をデータベースに保存（コミット）

# デバッグ用：テーブルの全行を取得
cursor.execute("SELECT * FROM my_table")
rows = cursor.fetchall()
print("ROWS", rows)  # 全データを一括表示

# 各行を個別に表示（見やすさのため）
for row in rows:
    print(row)

# データベース接続を閉じる
conn.close()

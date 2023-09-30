import sqlite3

# TW系テーブルクリア
conn = sqlite3.connect("database/database.db")
cur = conn.cursor()
sql = """
    DELETE FROM TPrintWork;
    DELETE FROM TW内訳別申請台数;
    DELETE FROM TW内訳別保有台数;
    DELETE FROM TW車格別保有台数;
    DELETE FROM TW申請車両;
    """
cur.executescript(sql)
conn.commit()

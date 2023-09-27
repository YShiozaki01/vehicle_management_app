import PySimpleGUI as sg
import sqlite3

sg.theme("SystemDefault")
DATABASE = "database/database.db"


# データベースに接続
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

class PrtdataGen:
    def __init__(self, prt_conditions):
        self.prt_conditions = prt_conditions

    # 部署別保有台数
    def number_of_dept(self):
        sql = """
            SELECT sum(existence) as number, department FROM T車両履歴 GROUP by department;
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    # 部署別内訳別保有台数
    def number_of_class(self):
        sql = """
            SELECT department, classification, sum(existence) as number FROM
            (SELECT a.company_use_number, a.classification, b.department, a.existence
            FROM T車両台帳 as a
            LEFT JOIN (SELECT * FROM T車両履歴 WHERE existence = 1) as b
            on a.company_use_number = b.company_use_number)
            GROUP by department, classification;
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result
    
    # 部署別車格別保有台数
    def number_of_size(self):
        sql = """
            SELECT department, car_size, sum(existence) as number FROM
            (SELECT a.company_use_number, a.car_size, b.department, a.existence
            FROM T車両台帳 as a
            LEFT JOIN (SELECT * FROM T車両履歴 WHERE existence = 1) as b
            on a.company_use_number = b.company_use_number)
            GROUP by department, car_size;
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    # TPrintWorkへ作成条件を挿入
    def insert_pw(self):
        sql = """"""
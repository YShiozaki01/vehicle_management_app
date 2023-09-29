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
        self.company_use_number = prt_conditions[0]
        self.implementation_date = prt_conditions[1]
        self.department = prt_conditions[2]
        self.circumstances = prt_conditions[3]

    # 部署別保有台数
    def number_of_dept(self):
        sql = f"""
            SELECT sum(existence) as number, department FROM T車両履歴
            GROUP by department
            WHERE department = '{self.department};'
            """
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    # 部署別内訳別保有台数
    def number_of_class(self):
        sql = """
            INSERT INTO TW内訳別台数 (
            SELECT department, classification, sum(existence) as number FROM
            (SELECT a.company_use_number, a.classification, b.department, a.existence
            FROM T車両台帳 as a
            LEFT JOIN (SELECT * FROM T車両履歴 WHERE existence = 1) as b
            on a.company_use_number = b.company_use_number)
            GROUP by department, classification
            );
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    
    # 部署別車格別保有台数
    def number_of_size(self):
        sql = """
            INSERT INTO TW車格別台数 (
            SELECT department, car_size, sum(existence) as number FROM
            (SELECT a.company_use_number, a.car_size, b.department, a.existence
            FROM T車両台帳 as a
            LEFT JOIN (SELECT * FROM T車両履歴 WHERE existence = 1) as b
            on a.company_use_number = b.company_use_number)
            GROUP by department, car_size
            );
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    # 申請車両情報
    def application_vehicle(self):
        if self.circumstances == "T":
            dept_org = self.get_dept_org()
            dept_org_code = dept_org[2]
            dept_org_name = dept_org[3]
        else:
            dept_org_code = ""
            dept_org_name = ""
        incr_decr = self.get_incr_decr()
        sql = f"""
            INSERT INTO TW申請車両 
            SELECT
            a.company_use_number,
            b.circumstances,
            b.department,
            c.official_use_name,
            a.classification,
            d.name as class_name,
            a.maker,
            a.model_year,
            a.load_capacity,
            a.body_number,
            e.basis_of_use || class_number || hiragana || designated_number as reg_no,
            a.specification,
            '{dept_org_code}',
            '{dept_org_name}',
            a.riding_capacity,
            a.existence,
            '{incr_decr}'
            FROM T車両台帳 as a"""
        if self.circumstances == "D":
            sql += f""" LEFT JOIN (SELECT * FROM T車両履歴
                    WHERE id = (SELECT max(id) FROM T車両履歴
                    WHERE company_use_number = '{self.company_use_number}')) as b"""
        else:
            sql += " LEFT JOIN (SELECT * FROM T車両履歴 WHERE existence =1) as b"
        sql += """ on a.company_use_number = b.company_use_number
                LEFT JOIN M部署 as c on b.department = c.code
                LEFT JOIN M種別 as d on a.classification = d.code"""
        if self.circumstances == "D":
            sql += f""" LEFT JOIN (SELECT * FROM T登録番号 
                    WHERE id = (SELECT max(id) FROM T登録番号
                    WHERE company_use_number = '{self.company_use_number}')) as e
                    on a.company_use_number = e.company_use_number"""
        else:
            sql += """ LEFT JOIN (SELECT * FROM T登録番号 WHERE existence = 1) as e
                on a.company_use_number = e.company_use_number"""
        sql += f" WHERE a.company_use_number = '{self.company_use_number}';"
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    
    # 増減区分を取得
    def get_incr_decr(self):
        if self.circumstances in ("A", "T"):
            incr_decr = "I"
        elif self.circumstances in ("D", "F"):
            incr_decr = "D"
        return incr_decr

    # 直近の移動元履歴を取得
    def get_dept_org(self):
        sql = f"""
            SELECT a.id, a.company_use_number, a.department, b.official_use_name as dept_name,
            a.circumstances
            FROM T車両履歴 as a
            LEFT JOIN M部署 as b on a.department = b.code
            WHERE a.id =
            (SELECT max(id) FROM T車両履歴 WHERE company_use_number = '{self.company_use_number}'
            AND circumstances = 'F');
            """
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result

    # TPrintWorkへ作成条件を挿入
    def insert_pw(self):
        sql = """
            INSERT INTO TPrintWork VALUES(?, ?, ?, ?);
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql, self.prt_conditions)
        conn.commit()

    # 申請営業所のリストを取得
    def get_application_dept(self):
        sql = "SELECT department FROM TW申請車両 GROUP by department;"
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        dept_list = []
        for dept in result:
            dept_list.append(dept[0])
        return dept_list

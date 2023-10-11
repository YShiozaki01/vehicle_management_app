from flask import Flask, render_template, request
import sqlite3
import datetime
from fuel_efficiency import FuelEfficiency

app = Flask(__name__)

# DATABASE = "../荷物事故登録SV/database/database.db"
DATABASE = "./database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# T車両履歴テーブルに登録されている部署の一覧を取得する
def get_department_list():
    # データベース接続
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    sql = """
        SELECT a.department, b.name FROM (
        SELECT department FROM T車両履歴 GROUP by department
        ) as a
        LEFT JOIN M部署 as b
        on a.department = b.code;
        """
    cur.execute(sql)
    dept_list = cur.fetchall()
    return dept_list


# T車両履歴テーブルから入力した検索キーで検索したレコードを抽出する
def get_search_record(search_keys):
    key1 = search_keys["dept_cd"]               # 部署コード
    key2 = search_keys["company_use_number"]    # 社番（一部）
    key3 = search_keys["reg_number"]            # 車両番号（一部）
    key4 = search_keys["body_number"]           # 車体番号（一部）
    sql = f"""
        SELECT a.department, c.name as dept_name, b.company_use_number,
        d.reg_number, b.body_number
        FROM (SELECT a2.* FROM
        (SELECT max(id) as max_id FROM T車両履歴
        GROUP by company_use_number) as a1
        LEFT JOIN T車両履歴 as a2
        on a1.max_id = a2.id) as a
        LEFT JOIN T車両台帳 as b
        on a.company_use_number = b.company_use_number
        LEFT JOIN M部署 as c on a.department = c.code
        LEFT JOIN (
        SELECT company_use_number,
        basis_of_use || class_number || hiragana || designated_number
        as reg_number FROM T登録番号 GROUP by company_use_number) as d
        on a.company_use_number = d.company_use_number
        WHERE a.company_use_number like '%{key2}%'
        AND a.department like '%{key1}%'
        AND b.body_number like '%{key4}%'
        AND d.reg_number like '%{key3}%';
         """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    if len(cur.fetchall()) == 0:
        result = "emptiness"
    else:
        cur.execute(sql)
        result = cur.fetchall()
    return result


@app.route("/")
def index():
    dept_list = get_department_list()
    return render_template("main.html", dept_list=dept_list)


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        keys = request.form.to_dict()
        # 部署コード
        if not "dept" in keys:
            dept_cd = "%"
        else:
            dept_cd = keys["dept"]
        # 社番（一部）
        if keys["company_use_number"] == "":
            company_use_number = "%"
        else:
            company_use_number = keys["company_use_number"]
        # 車両番号（一部）
        if keys["reg_number"] == "":
            reg_number = "%"
        else:
            reg_number = keys["reg_number"]
        # 車体番号（一部）
        if not "body_number" in keys:
            body_number = "%"
        else:
            body_number = keys["body_number"]
        search_keys = {
            "dept_cd": dept_cd,
            "company_use_number": company_use_number,
            "reg_number": reg_number,
            "body_number": body_number,
        }
        records = get_search_record(search_keys)
        return render_template("main.html", records=records)


@app.route("/show_detail/<code>")
def show_detail(code):
    # 指定車両の履歴を取得
    sql = f"""
        SELECT a.implementation_date,
        CASE
        WHEN a.circumstances = 'A' THEN '導入'
        WHEN a.circumstances = 'F' THEN '移動（元）'
        WHEN a.circumstances = 'T' THEN '移動（先）'
        WHEN a.circumstances = 'D' THEN '廃止'
        END as situation,
        a.department,
        b.name
        FROM T車両履歴 as a
        LEFT JOIN M部署 as b
        on a.department = b.code
        WHERE a.company_use_number = '{code}'
        ORDER by id;
        """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql)
    result = list(cur.fetchall())
    # 本年度の年数を取得
    str_now = datetime.datetime.now()
    this_year = int(str_now.strftime('%Y'))
    # 本年度年間の走行距離と燃料使用量を取得して変数に追加
    fe = FuelEfficiency(this_year, code)
    fuel_data = []
    # 1)年間走行距離
    # 直近の走行距離を取得
    data = fe.lastest_meter()
    if data == None:
        lastest_meter = 0
    else:
        lastest_meter = data["meter"]
    # 前年度末の走行距離を取得
    data = fe.start_meter()
    if data == None:
        start_meter = 0
    else:
        start_meter = data["meter"]
    # 本年度の年間走行距離を取得
    annual_mileage = lastest_meter - start_meter
    fuel_data.append(annual_mileage)
    # 2)年間燃料使用量
    fuel_efficiency = fe.fuel_efficiency()
    fuel_data.append(fuel_efficiency)
    return render_template("detail_record.html", cun=code,
                           hist=result, fuel_data=fuel_data)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5001")

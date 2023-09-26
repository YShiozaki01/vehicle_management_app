import PySimpleGUI as sg
import sqlite3
import datetime
from select_item import SelectItem, SelectVehicle

sg.theme("SystemDefault")
DATABASE = "database/database.db"
SQL_DEPT = "SELECT code, name FROM M部署;"
SQL_SITUATION = "SELECT code, name FROM M状況;"
SQL_CARSIZE = "SELECT code, name FROM M車格;"
SQL_CARTYPE = "SELECT code, name FROM M種別;"


# SQLのSELECT文で辞書型でレコードを取得するDB接続
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# テーブルの最新ID番号を取得
def get_id_number(table_name):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    sql1 = f"""
        SELECT * FROM {table_name};
        """
    cur.execute(sql1)
    if len(cur.fetchall()) == 0:
        new_id = 1
    else:
        sql = f"""
            SELECT max(id) FROM {table_name};
            """
        cur.execute(sql)
        result = cur.fetchone()
        new_id = result[0] + 1
    return new_id


# 車両3テーブルのデータを取得
def get_recd(table_name, cun="%", ):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = f"""
        SELECT * FROM {table_name} WHERE company_use_number = '{cun}' and existence = 1;
        """
    cur.execute(sql)
    result = cur.fetchone()
    return result


# 入力フォームに再セットするデータを生成
def get_reset_data(company_use_number):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = f"""
            SELECT
                a.company_use_number,
                a.classification,
                b.name as class_name,
                a.maker,
                a.model_number,
                a.body_number,
                a.model_year,
                a.car_size,
                c.name as size_name,
                a.load_capacity,
                a.specification,
                a.riding_capacity,
                a.fuel_type,
                d.department,
                d.implementation_date,
                d.circumstances,
                e.name as dept_name,
                f.basis_of_use,
                f.class_number,
                f.hiragana,
                f.designated_number
            FROM T車両台帳 as a
            LEFT JOIN M種別 as b on a.classification = b.code
            LEFT JOIN M車格 as c on a.car_size = c.code
            LEFT JOIN T車両履歴 as d on a.company_use_number = d.company_use_number
            LEFT JOIN M部署 as e on d.department = e.code
            LEFT JOIN T登録番号 as f on a.company_use_number = f.company_use_number
            WHERE a.company_use_number = '{company_use_number}'
            and d.existence = 1
            and f.existence = 1;
        """
    cur.execute(sql)
    result = cur.fetchone()
    return result


# 全入力フィールドをクリア
def clear_all():
    window["-correction-"].update(disabled=True)
    window["-transfer_abolition-"].update(disabled=True)
    window["-in1-"].update("")
    window["-cd2-"].update("")
    window["-in3-"].update("")
    window["-in4-"].update("")
    window["-in5-"].update("")
    window["-in6-"].update("")
    window["-in7-"].update("")
    window["-cd3-"].update("")
    window["-in8-"].update("")
    window["-in9-"].update("")
    window["-in10-"].update("")
    window["-in11-"].update("")
    window["-in12-"].update("")
    window["-in1f-"].update("")
    window["-in2f-"].update("")
    window["-in3f-"].update("")
    window["-in4f-"].update("")
    window["-cd1-"].update("")
    window["-in2-"].update("")
    window["-in13-"].update("")
    window["-cd4-"].update("")


# 指定した社番で、実在の車両レコードが存在するか
def check_number(company_use_number):
    sql = f"""
        SELECT * FROM T車両台帳 WHERE company_use_number = '{company_use_number}';  
        """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql)
    if len(cur.fetchall()) == 0:
        result = False
    else:
        result = True
    return result


# 3テーブルに入力データを挿入
def insert_data(signup):
    new_id1 = get_id_number("T車両台帳")
    new_id2 = get_id_number("T登録番号")
    new_id3 = get_id_number("T車両履歴")
    now_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # T車両台帳テーブルに挿入するデータを生成
    car_info = []
    car_info.append(new_id1)        # T車両台帳<id>
    car_info.append(v["-in1-"])     # T車両台帳<company_use_number>
    car_info.append(v["-cd2-"])     # T車両台帳<classification>
    car_info.append(v["-in4-"])     # T車両台帳<maker>
    car_info.append(v["-in5-"])     # T車両台帳<model_number>
    car_info.append(v["-in6-"])     # T車両台帳<body_number>
    car_info.append(v["-in7-"])     # T車両台帳<model_year>
    car_info.append(v["-cd3-"])     # T車両台帳<car_size>
    car_info.append(v["-in9-"])     # T車両台帳<load_capacity>
    car_info.append(v["-in10-"])    # T車両台帳<specification>
    car_info.append(v["-in11-"])    # T車両台帳<riding_capacity>
    car_info.append(v["-in12-"])    # T車両台帳<fuel_type>
    car_info.append(1)              # T車両台帳<existence>
    car_info.append(now_dt)         # T車両台帳<update_date>
    # T登録番号テーブルに挿入するデータを生成
    reg_num = []
    reg_num.append(new_id2)         # T登録番号<id>
    reg_num.append(v["-in1-"])      # T登録番号<company_use_number>
    reg_num.append(v["-in1f-"])     # T登録番号<basis_of_use>
    reg_num.append(v["-in2f-"])     # T登録番号<class_number>
    reg_num.append(v["-in3f-"])     # T登録番号<hiragana>
    reg_num.append(v["-in4f-"])     # T登録番号<designated_number>
    reg_num.append(1)               # T登録番号<existence>
    reg_num.append(now_dt)          # T登録番号<update_date>
    # T車両履歴テーブルに挿入するデータを生成
    car_hist = []
    car_hist.append(new_id3)        # T車両履歴<id>
    car_hist.append(v["-in1-"])     # T車両履歴<company_use_number>
    car_hist.append(v["-cd1-"])     # T車両履歴<department>
    if signup:
        car_hist.append(v["-cd4-"]) # T車両履歴<circumstances>（修正）
    else:
        car_hist.append("A")        # T車両履歴<circumstances>（新規）
    car_hist.append(v["-in13-"])    # T車両履歴<implementation_date>
    car_hist.append(1)              # T車両履歴<existence>
    car_hist.append(now_dt)         # T車両履歴<update_date>
    # テーブルにデータを挿入
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    sql1 = f"""
        INSERT INTO T車両台帳 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    sql2 = f"""
        INSERT INTO T登録番号 VALUES(?, ?, ?, ?, ?, ?, ?, ?);
        """
    sql3 = f"""
        INSERT INTO T車両履歴 VALUES(?, ?, ?, ?, ?, ?, ?);
        """
    cur.execute(sql1, car_info)
    cur.execute(sql2, reg_num)
    cur.execute(sql3, car_hist)
    conn.commit()


# テーブルからレコードを削除
def delete_data(company_use_number):
    sql = f"""
        DELETE FROM T車両台帳 WHERE company_use_number = '{company_use_number}'
        and existence = 1;
        DELETE FROM T車両履歴 WHERE company_use_number = '{company_use_number}'
        and existence = 1;
        DELETE FROM T登録番号 WHERE company_use_number = '{company_use_number}'
        and existence = 1;
        """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.executescript(sql)
    conn.commit()


# T車両台帳とT登録番号から    
# ウインドウレイアウト
frame_layout = [[sg.T("使用の本拠", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in1f-", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("分類番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in2f-", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("ひらがな", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in3f-", size=(5, 0), font=("Yu Gothic UI", 8))],
                [sg.T("指定番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in4f-", size=(10, 0), font=("Yu Gothic UI", 8))]]
layout = [[sg.T("車両入力", font=("Yu Gothic UI", 11)),],
        [sg.T("社番", size=(10, 0), font=("Yu Gothic UI", 8), text_color="#FF0000"),
         sg.I(k="-in1-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("部署", size=(10, 0), font=("Yu Gothic UI", 8), text_color="#FF0000"),
         sg.B("検索", k="-btn1-", font=("Yu Gothic UI", 8)),
         sg.I(k="-in2-", font=("Yu Gothic UI", 8), size=(20, 0), readonly=True),
         sg.I(k="-cd1-", font=("Yu Gothic UI", 8), size=(4, 0), visible=False)],
        [sg.T("内訳", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.B("検索", k="-btn2-", font=("Yu Gothic UI", 8)),
         sg.I(k="-in3-", font=("Yu Gothic UI", 8), size=(20, 0), readonly=True),
         sg.I(k="-cd2-", font=("Yu Gothic UI", 8), size=(4, 0), visible=False)],
        [sg.T("車名", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="-in4-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("型式", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="-in5-", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("車体番号", size=(10, 0), font=("Yu Gothic UI", 8), text_color="#FF0000"),
        sg.I(k="-in6-", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("年式", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="-in7-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("車格", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.B("検索", k="-btn3-", font=("Yu Gothic UI", 8)),
         sg.I(k="-in8-", font=("Yu Gothic UI", 8), size=(20, 0), readonly=True),
         sg.I(k="-cd3-", font=("Yu Gothic UI", 8), size=(4, 0), visible=False)],
        [sg.T("最大積載量", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in9-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("形状", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in10-", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("乗車定員", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in11-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("燃料種類", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in12-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("実施日", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in13-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.Frame(title="登録番号", font=("Yu Gothic UI", 8), layout=frame_layout),
         sg.I(k="-cd4-", font=("Yu Gothic UI", 8), size=(4, 0), visible=False),
         sg.B("検索", k="-btn_search-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.Radio("修正", group_id="destination", font=("Yu Gothic UI", 8), key="-correction-",
                  disabled=True, default=True),
         sg.Radio("移動・廃止", group_id="destination", font=("Yu Gothic UI", 8), key="-transfer_abolition-",
                  disabled=True),
         sg.Push(), sg.B("登録", k="-btn_register-", size=(10, 0), font=("Yu Gothic UI", 8))]]
window = sg.Window("車両入力", layout, font=("Yu Gothic UI", 8),
                size=(300, 500), disable_close=False)
window.finalize()

selection_mode = False
while True:
    e, v = window.read()
    if e == "-btn1-":
        si1 = SelectItem(SQL_DEPT)
        items = si1.open_sub_window()
        if items:
            window["-in2-"].update(items[1])
            window["-cd1-"].update(items[0])
    if e == "-btn2-":
        si2 = SelectItem(SQL_CARTYPE)
        items = si2.open_sub_window()
        if items:
            window["-in3-"].update(items[1])
            window["-cd2-"].update(items[0])
    if e == "-btn3-":
        si3 = SelectItem(SQL_CARSIZE)
        items = si3.open_sub_window()
        if items:
            window["-in8-"].update(items[1])
            window["-cd3-"].update(items[0])
    if e == "-btn_register-":
        if not selection_mode:
            reality = check_number(v["-in1-"])
            if reality == True:
                sg.popup("登録済みの車番です。", title="確認", font=("Yu Gothic UI", 8))
            else:
                insert_data(selection_mode)
        if selection_mode:
            if v["-correction-"]:
                delete_data(v["-in1-"])
                insert_data(selection_mode)
            elif v["-transfer_abolition-"]:
                print("「移動・廃止」工事中")
            selection_mode = False
        clear_all()
    if e == "-btn_search-":
        selection_mode = True
        company_use_number = v["-in1-"] if v["-in1-"] else "%"
        body_number = v["-in6-"] if v["-in6-"] else "%"
        department = v["-cd1-"] if v["-cd1-"] else "%"
        sv = SelectVehicle(company_use_number, body_number, department)
        vinfo = sv.open_sub_window()
        if vinfo:
            window["-correction-"].update(disabled=False)
            window["-transfer_abolition-"].update(disabled=False)
            record = get_reset_data(vinfo[0])
            window["-in1-"].update(record["company_use_number"])
            window["-cd2-"].update(record["classification"])
            window["-in3-"].update(record["class_name"])
            window["-in4-"].update(record["maker"])
            window["-in5-"].update(record["model_number"])
            window["-in6-"].update(record["body_number"])
            window["-in7-"].update(record["model_year"])
            window["-cd3-"].update(record["car_size"])
            window["-in8-"].update(record["size_name"])
            window["-in9-"].update(record["load_capacity"])
            window["-in10-"].update(record["specification"])
            window["-in11-"].update(record["riding_capacity"])
            window["-in12-"].update(record["fuel_type"])
            window["-in1f-"].update(record["basis_of_use"])
            window["-in2f-"].update(record["class_number"])
            window["-in3f-"].update(record["hiragana"])
            window["-in4f-"].update(record["designated_number"])
            window["-cd1-"].update(record["department"])
            window["-in2-"].update(record["dept_name"])
            window["-in13-"].update(record["implementation_date"])
            window["-cd4-"].update(record["circumstances"])
    if e == None:
        break
window.close()
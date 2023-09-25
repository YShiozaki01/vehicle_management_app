import PySimpleGUI as sg
import sqlite3
from select_item import SelectItem

sg.theme("SystemDefault")
DATABASE = "database/database.db"
SQL_DEPT = "SELECT code, name FROM M部署;"
SQL_SITUATION = "SELECT code, name FROM M状況;"
SQL_CARSIZE = "SELECT code, name FROM M車格;"
SQL_CARTYPE = "SELECT code, name FROM M種別;"


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


# ウインドウレイアウト
frame_layout = [[sg.T("使用の本拠", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in1f-", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("分類番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in2f-", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("ひらがな", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in3f-", size=(5, 0), font=("Yu Gothic UI", 8))],
                [sg.T("指定番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                 sg.I(k="-in4f-", size=(10, 0), font=("Yu Gothic UI", 8))]]
layout = [[sg.T("車両入力", font=("Yu Gothic UI", 11))],
        [sg.T("社番", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in1-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("部署", size=(10, 0), font=("Yu Gothic UI", 8)),
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
        [sg.T("車体番号", size=(10, 0), font=("Yu Gothic UI", 8)),
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
        [sg.T("乗車定員", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in11-", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("燃料種類", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in12-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("実施日", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.I(k="-in13-", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.Frame(title="登録番号", font=("Yu Gothic UI", 8), layout=frame_layout)],
        [sg.B("検索", k="-btn_search-", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.Push(),
         sg.B("登録", k="-btn_register-", size=(10, 0), font=("Yu Gothic UI", 8))]]
window = sg.Window("車両入力", layout, font=("Yu Gothic UI", 8),
                size=(300, 500), disable_close=False)
window.finalize()

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
        new_id = get_id_number()
        date = 
        car_info = []
        car_info.append(new_id)         # T車両台帳<id>
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
    if e == None:
        break
window.close()
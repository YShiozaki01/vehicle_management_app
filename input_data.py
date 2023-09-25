import PySimpleGUI as sg
from select_item import SelectItem

sg.theme("SystemDefault")
DATABASE = "database/vehicle.db"
SQL_DEPT = "SELECT code, name FROM M部署;"
SQL_SITUATION = "SELECT code, name FROM M状況;"
SQL_CARSIZE = "SELECT code, name FROM M車格;"
SQL_CARTYPE = "SELECT code, name FROM M種別;"


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
         sg.I(k="-in1-", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.Push(),
         sg.B("検索", k="-btn1-", font=("Yu Gothic UI", 8))],
        [sg.T("部署", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.B("検索", k="-btn2-", font=("Yu Gothic UI", 8)),
         sg.I(k="-in2-", font=("Yu Gothic UI", 8), size=(20, 0), readonly=True),
         sg.I(k="-cd1-", font=("Yu Gothic UI", 8), size=(4, 0), visible=False)],
        [sg.T("内訳", size=(10, 0), font=("Yu Gothic UI", 8)),
         sg.B("検索", k="-btn3-", font=("Yu Gothic UI", 8)),
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
         sg.B("検索", k="-btn4-", font=("Yu Gothic UI", 8)),
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
        [sg.Frame(title="登録番号", font=("Yu Gothic UI", 8), layout=frame_layout)],
        [sg.Push(), sg.B("登録", k="btn_register", size=(10, 0), font=("Yu Gothic UI", 8))]]
window = sg.Window("車両入力", layout, font=("Yu Gothic UI", 8),
                size=(300, 500), disable_close=False)
window.finalize()

while True:
    e, v = window.read()
    if e == "-btn2-":
        si1 = SelectItem(SQL_DEPT)
        items = si1.open_sub_window()
        if items:
            window["-in2-"].update(items[1])
            window["-cd1-"].update(items[0])
    if e == "-btn3-":
        si2 = SelectItem(SQL_CARTYPE)
        items = si2.open_sub_window()
        if items:
            window["-in3-"].update(items[1])
            window["-cd2-"].update(items[0])
    if e == "-btn4-":
        si3 = SelectItem(SQL_CARSIZE)
        items = si3.open_sub_window()
        if items:
            window["-in8-"].update(items[1])
            window["-cd3-"].update(items[0])
    if e == None:
        break
window.close()
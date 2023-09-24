import PySimpleGUI as sg

sg.theme("SystemDefault")
DATABASE = "database/vehicle.db"


# ウインドウレイアウト
frame_layout = [[sg.T("使用の本拠", size=(10, 0), font=("Yu Gothic UI", 8)),
                sg.I(k="in4", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("分類番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                sg.I(k="in5", size=(10, 0), font=("Yu Gothic UI", 8))],
                [sg.T("ひらがな", size=(10, 0), font=("Yu Gothic UI", 8)),
                sg.I(k="in6", size=(5, 0), font=("Yu Gothic UI", 8))],
                [sg.T("指定番号", size=(10, 0), font=("Yu Gothic UI", 8)),
                sg.I(k="in7", size=(10, 0), font=("Yu Gothic UI", 8))]]
layout = [[sg.T("車両入力", font=("Yu Gothic UI", 11)), sg.Push(),
        sg.T("", k="txt1", font=("Yu Gothic UI", 10), text_color="#FFFFFF")],
        [sg.T("社番", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in1", size=(10, 0), font=("Yu Gothic UI", 8)), sg.Push(),
        sg.Checkbox("移動", k="chk1", font=("Yu Gothic UI", 9), text_color="#FF0000",
                    default=False, visible=False)],
        [sg.T("部署", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.Combo(values=list_department, font=("Yu Gothic UI", 8),
                    size=(20, 0), key='cmb1', readonly=True, enable_events=True),
        sg.I(font=("Yu Gothic UI", 8), size=(4, 0), k="cd1", visible=False)],
        [sg.T("内訳", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.Combo(values=list_classification, font=("Yu Gothic UI", 8),
                    size=(20, 0), key='cmb2', readonly=True, enable_events=True),
        sg.I(font=("Yu Gothic UI", 8), size=(4, 0), k="cd2", visible=False)],
        [sg.T("車名", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in2", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("年式", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in3", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.T("最大積載量", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in8", size=(10, 0), font=("Yu Gothic UI", 8))],
        [sg.T("型式", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in9", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("車体番号", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in10", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("形状", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.I(k="in11", size=(30, 0), font=("Yu Gothic UI", 8))],
        [sg.T("車格", size=(10, 0), font=("Yu Gothic UI", 8)),
        sg.Combo(values=list_carsize, font=("Yu Gothic UI", 8),
                    size=(20, 0), key='cmb3', readonly=True, enable_events=True),
        sg.I(font=("Yu Gothic UI", 8), size=(4, 0), k="cd3", visible=False)],
        [sg.T("実施日", size=(10, 0), font=("Yu Gothic UI", 8)),
            sg.I(k="in12", size=(20, 0), font=("Yu Gothic UI", 8))],
        [sg.Frame(title="登録番号", font=("Yu Gothic UI", 8), layout=frame_layout)],
        [sg.T("", font=("Yu Gothic UI", 8))],
        [sg.B("廃止", k="btn_delete", size=(10, 0), font=("Yu Gothic UI", 8),
            button_color=("#FFFFFF", "#FF0000"), visible=False),
        sg.Push(), sg.B("登録", k="btn_register", size=(10, 0), font=("Yu Gothic UI", 8))]
        ]
window = sg.Window("車両入力", layout, font=("Yu Gothic UI", 8),
                size=(280, 460), disable_close=False)
window.finalize()

while True:
    e, v = window.read()
    if e == None:
        break
window.close()
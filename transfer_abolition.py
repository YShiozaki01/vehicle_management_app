import PySimpleGUI as sg
import sqlite3
import datetime
import pandas as pd
from select_item import SelectItem

sg.theme("SystemDefault")
DATABASE = "database/database.db"
TABLE1 = "T車両履歴"
TABLE2 = "T車両台帳"
TABLE3 = "T登録番号"
SQL_DEPT = "SELECT code, name FROM M部署;"


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


# 8桁数字を日付に変換
def change_date(value):
    # 入力された値が8桁数字かチェック（数値ではなく整数文字か判定）
    target = value
    if target.isdigit() and len(target) == 8:
        date = pd.to_datetime(target)
        format_date = format(date, "%Y/%m/%d")
    else:
        format_date = ""
    return format_date


class TrfAbol:
    def __init__(self, company_use_number, dept_name_from, dept_code_from):
        self.company_use_number = company_use_number
        self.dept_name_from = dept_name_from
        self.dept_code_from = dept_code_from

    def open_sub_window2(self):
        # レイアウト
        layout = [
            [sg.T("実施日", font=("Yu Gothic UI", 8)), sg.I(k="-impl_date-", size=(10, 0), font=("Yu Gothic UI", 8))],
            [sg.Radio("移動", group_id="process2", font=("Yu Gothic UI", 8), key="-transfer-",
                      disabled=False, default=True),
            sg.I(k="-in_from-", size=(10, 0), font=("Yu Gothic UI", 8), default_text=self.dept_name_from,
                 disabled=True),
            sg.T("ー＞", font=("Yu Gothic UI", 8)),
            sg.I(k="-in_to-", size=(10, 0), font=("Yu Gothic UI", 8), disabled=True),
            sg.B("検索", k="-btn_search-", font=("Yu Gothic UI", 8))],
            [sg.Radio("廃止", group_id="process2", font=("Yu Gothic UI", 8), key="-abolition-",
                     disabled=False)],
            [sg.I(k="-cd_from-", size=(4, 0), font=("Yu Gothic UI", 8), default_text=self.dept_code_from,
                  disabled=True, visible=False),
             sg.I(k="-cd_to-", size=(4, 0), font=("Yu Gothic UI", 8), disabled=True, visible=False),
             sg.Push(), sg.B("登録", k="-btn_register-", size=(10, 0), font=("Yu Gothic UI", 8))]
        ]
        window = sg.Window("車両履歴更新", layout, font=("Yu Gothic UI", 8), size=(300, 120), disable_close=False)
        window.finalize()
        # エンターキー押下
        window["-impl_date-"].bind("<Return>", "_r")
        window["-transfer-"].bind("<Return>", "_r")
        window["-btn_search-"].bind("<Return>", "_r")
        window["-abolition-"].bind("<Return>", "_r")
        window["-btn_register-"].bind("<Return>", "_r")
        # 動作
        while True:
            e, v = window.read()
            if e == "-impl_date-_r":
                # strdate = change_date(v["-impl_date-"])
                # if strdate == "":
                #     sg.popup("8桁数字で入力してください", font=("Yu Gothic UI", 8))
                # else:
                #     window["-impl_date-"].update(strdate)
                    window["-transfer-"].set_focus(True)
            if e == "-transfer-_r":
                window["-btn_search-"].set_focus(True)
            if e == "-btn_search-_r":
                window["-abolition-"].set_focus(True)
            if e == "-abolition-_r":
                window["-btn_register-"].set_focus(True)
            if e == "-btn_search-":
                si = SelectItem(SQL_DEPT)
                items = si.open_sub_window()
                if items:
                    window["-in_to-"].update(items[1])
                    window["-cd_to-"].update(items[0])
            if e == "-btn_register-":
                # 日付をスラッシュ区切りに変換（エンターキー押下し忘れ対策）
                strdate = change_date(v["-impl_date-"])
                if strdate == "":
                    sg.popup("8桁数字で入力してください", font=("Yu Gothic UI", 8))
                else:
                    if v["-transfer-"]:
                        # データベース接続
                        conn = sqlite3.connect(DATABASE)
                        cur = conn.cursor()
                        # 更新日を取得
                        now_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # 挿入データリストを生成
                        new_id1 = get_id_number(TABLE1)
                        new_id2 = new_id1 + 1
                        list_org = [new_id1, self.company_use_number, v["-cd_from-"], "F", strdate, 0, now_dt]
                        list_dst = [new_id2, self.company_use_number, v["-cd_to-"], "T", strdate, 1, now_dt]
                        # T車両履歴の同車両のexistenceを0に更新
                        sql1 = f"""
                            UPDATE {TABLE1} SET existence = 0
                            WHERE company_use_number = '{self.company_use_number}'
                            and existence = 1;
                            """
                        cur.execute(sql1)
                        # T車両履歴にレコードを追加
                        sql2 = f"""
                            INSERT INTO {TABLE1} VALUES(?, ?, ?, ?, ?, ?, ?);
                            """
                        # 1)移動元
                        cur.execute(sql2, list_org)
                        # 2)移動先
                        cur.execute(sql2, list_dst)
                        conn.commit()
                        # 処理完了メッセージ
                        sg.popup(f"社番{self.company_use_number}を{v['-in_from-']}から{v['-in_to-']}に移管しました。",
                                font=("Yu Gothic UI", 8), title="完了")
                        break
                    elif v["-abolition-"]:
                        # データベース接続
                        conn = sqlite3.connect(DATABASE)
                        cur = conn.cursor()
                        # 更新日を取得
                        now_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # 挿入データリストを生成
                        new_id = get_id_number(TABLE1)
                        list_del = [new_id, self.company_use_number, v["-cd_from-"], "D", strdate, 0, now_dt]
                        # 3テーブルの同車両のexistenceを0に更新
                        sql1 = f"""
                            UPDATE {TABLE1} SET existence = 0
                            WHERE company_use_number = '{self.company_use_number}'
                            and existence = 1;
                            UPDATE {TABLE2} SET existence = 0, update_date = '{now_dt}'
                            WHERE company_use_number = '{self.company_use_number}';
                            UPDATE {TABLE3} SET existence = 0, update_date = '{now_dt}'
                            WHERE company_use_number = '{self.company_use_number}'
                            and existence = 1;
                            """
                        cur.executescript(sql1)
                        # T車両履歴にレコードを追加
                        sql2 = f"""
                            INSERT INTO {TABLE1} VALUES(?, ?, ?, ?, ?, ?, ?);
                            """
                        cur.execute(sql2, list_del)
                        conn.commit()
                        # 処理完了メッセージ
                        sg.popup(f"社番{self.company_use_number}を廃止しました。", font=("Yu Gothic UI", 8), title="完了")
                        break
            if e == None:
                break
        window.close()
    
if __name__ == "__main__":
    ta = TrfAbol("221127", "戸田", "03")
    ta.open_sub_window2()
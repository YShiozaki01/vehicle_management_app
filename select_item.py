import PySimpleGUI as sg
import sqlite3

sg.theme("SystemDefault")
DATABASE = "database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


class SelectItem:
    def __init__(self, sql):
        self.sql = sql

    def get_list(self):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(self.sql)
        result = cur.fetchall()
        return result

    def open_sub_window(self):
        item_list = self.get_list()
        layout = [
            [sg.Table(item_list, ["ID", "NAME"], font=("Yu Gothic UI", 10), justification="left", col_widths=(8, 20),
                    auto_size_columns=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE, num_rows=None,
                    k="-slc-", enable_events=True)],
            [sg.Push(), sg.B("キャンセル", font=("Yu Gothic UI", 9), size=(10, 0), k="-btn_cancel-"),]
        ]
        win = sg.Window("選択", layout, font=("Yu Gothic UI", 10), size=(250, 240), disable_close=True)
        win.finalize()

        while True:
            e, v = win.read()
            if e == "-slc-":
                item = item_list[v["-slc-"][0]]
                break
            if e == "-btn_cancel-":
                item = ""
                break
        win.close()
        return item

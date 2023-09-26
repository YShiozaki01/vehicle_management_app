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
                    k="-slc-", enable_events=True)]
        ]
        win = sg.Window("選択", layout, font=("Yu Gothic UI", 10), size=(250, 220), disable_close=False)
        win.finalize()
        while True:
            e, v = win.read()
            if e == "-slc-":
                item = item_list[v["-slc-"][0]]
                break
            if e == None:
                item = ""
                break
        win.close()
        return item

class SelectVehicle:
    def __init__(self, company_use_number, body_number, department):
        self.company_use_number = company_use_number
        self.body_number = body_number
        self.department = department

    def get_record_1(self):
        conn = get_db_connection()
        cur = conn.cursor()
        sql = f"""
            SELECT a.*, b.department, c.name as dept_name FROM T車両台帳 as a
            LEFT JOIN T車両履歴 as b
            on a.company_use_number = b.company_use_number
            LEFT JOIN M部署 as c on b.department = c.code
            WHERE a.company_use_number like '%{self.company_use_number}%'
            and a.body_number like '%{self.body_number}%'
            and b.department like '%{self.department}%'
            and b.existence = 1;
            """
        cur.execute(sql)
        result = cur.fetchall()
        items = []
        for row in result:
            r = []
            r.append(row["company_use_number"])
            r.append(row["body_number"])
            r.append(row["dept_name"])
            items.append(r)
        return items

    def open_sub_window(self):
        items = self.get_record_1()
        layout = [
            [sg.Table(items, ["CODE", "BODYNUMBER", "DEPT"], font=("Yu Gothic UI", 10), justification="left", col_widths=(8, 20),
                    auto_size_columns=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE, num_rows=None,
                    k="-slc-", enable_events=True)]
        ]
        win = sg.Window("選択", layout, font=("Yu Gothic UI", 10), size=(350, 220), disable_close=False)
        win.finalize()
        while True:
            e, v = win.read()
            if e == "-slc-":
                item = items[v["-slc-"][0]]
                break
            if e == None:
                item = ""
                break
        win.close()
        return item
    

if __name__ == "__main__":
    sv = SelectVehicle()
    rec = sv.open_sub_window()
    print(rec)

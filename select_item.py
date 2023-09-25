import PySimpleGUI as sg
import sqlite3

sg.theme("SystemDefault")
DATABASE = "database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


class SelectItem:
    def __init__(self):
        self.sql_dept = "SELECT code, name FROM M部署;"
        self.sql_situation = "SELECT code, name FROM M状況;"
        self.sql_carsize = "SELECT code, name FROM M車格;"
        self.sql_cartype = "SELECT code, name FROM M種別;"

    def get_list(self, sql):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def make_itemlist(self):
        itemlist = self.get_list(self.sql_dept)
        return itemlist
    

if __name__ == "__main__":
    si = SelectItem()
    item_list = si.make_itemlist()
    print(item_list)
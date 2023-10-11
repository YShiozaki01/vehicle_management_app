import sqlite3
import datetime

DATABASE = "database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# 本年度を取得
def get_thisyear():
    str_now = datetime.datetime.now()
    this_year = int(str_now.strftime('%Y'))
    return this_year


class FuelEfficiency:
    def __init__(self, year, company_use_number):
        self.company_use_number = company_use_number
        self.this_year = year
    
    # T燃料使用量テーブルにおける指定社番の存在チェック
    def existence_check(self):
        sql = f"""
            SELECT * FROM T燃料使用量 
            WHERE company_use_number = '{self.company_use_number}'
            AND year || substr('0' || month, -2, 2) >= '{self.this_year}04'
            AND year || substr('0' || month, -2, 2) <= '{self.this_year + 1}03';
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        if len(cur.fetchall()) == 0:
            judgement = False
        else:
            judgement = True
        return judgement


    def lastest_meter(self):
        # 再直近の走行距離
        # T燃料使用量テーブルに指定社番のレコードがあれば
        if self.existence_check():
            sql = f"""
                select * from
                (select id, year || substr('0' || month, -2, 2) as year_m, 
                company_use_number, meter, fuel_usage
                from T燃料使用量
                where company_use_number ='{self.company_use_number}'
                and year_m >= '{self.this_year}04'
                and year_m <= '{str(self.this_year + 1)}03'
                and meter != 0)
                where id = 
                (select max(id) from
                (select * from T燃料使用量
                where company_use_number ='{self.company_use_number}'
                and year_m >= '{self.this_year}04'
                and year_m <= '{self.this_year + 1}03'
                and meter != 0));
                """
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()
        else:
            result = None
        return result

    def start_meter(self):
        # 起算月の走行距離
        # T燃料使用量テーブルに指定社番のレコードがあれば
        if self.existence_check():
            # 本年度以前の履歴があるか
            sql = f"""
                select * from T燃料使用量
                where company_use_number = '{self.company_use_number}'
                and meter != 0 and year || substr('0' || month, -2, 2) <= '{self.this_year}03';
                """
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute(sql)
            if len(cur.fetchall()) != 0:
                sql = f"""
                    select id, year || substr('0' || month, -2, 2) as year_m,
                    company_use_number, meter, fuel_usage
                    from T燃料使用量
                    where id = (select max(id) from
                    (select id from T燃料使用量 where company_use_number ='{self.company_use_number}'
                    and meter != 0 and year || substr('0' || month, -2, 2) <= '{self.this_year}03'));
                    """
            else:
                sql = f"""
                    select id, year || substr('0' || month, -2, 2) as year_m, 
                    company_use_number, meter, fuel_usage
                    from T燃料使用量
                    where id = (select min(id) from
                    (select id from T燃料使用量 where company_use_number ='{self.company_use_number}'
                    and meter != 0 and year || substr('0' || month, -2, 2) >= '{self.this_year}04'));
                    """
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()
        else:
            result = None
        return result

    def fuel_efficiency(self):
        # 年度中の燃料使用量を集計
        # T燃料使用量テーブルに指定社番のレコードがあれば
        if self.existence_check():
            sql = f"""
                select company_use_number, sum(fuel_usage) as fuel from T燃料使用量
                where company_use_number ='{self.company_use_number}'
                and year || substr('0' || month, -2, 2) >= '{self.this_year}04'
                and year || substr('0' || month, -2, 2) <= '{self.this_year + 1}03'
                group by company_use_number
                """
            
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()
            fuel = result['fuel']
        else:
            fuel = 0
        return fuel

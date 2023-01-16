from pymysql import *
from pickle import *


class PrfDAO:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.conn = connect(
            user=data["database"].get("user"),
            password=data["database"].get("password"),
            host=data["database"].get("host"),
            port=data["database"].get("port"),
            db=data["database"].get("db"),
            charset='utf8'
        )
        self.curs = self.conn.cursor(cursors.DictCursor)

    def insert_prf_data(self, data):
        sql = ("INSERT INTO performance VALUES (%(performance_id)s, " +
               "%(prf_title)s, %(prf_start_date)s, " +
               "%(prf_end_date)s, %(prf_cast)s, %(prf_crew)s, %(prf_runtime)s, " +
               "%(prf_prd_comp)s, %(prf_viewing_age)s, %(prf_ticket_price)s, " +
               "%(prf_poster)s, %(prf_story)s, %(prf_genre)s, %(prf_openrun)s, " +
               "%(prf_styurls)s, %(prf_state)s, %(prf_loaded_at)s, %(facility_id)s);")
        self.curs.executemany(sql, data)
        self.conn.commit()

    def select_prf_id_list(self):
        sql = "SELECT performance_id FROM performance"
        self.curs.execute(sql)
        list = []
        result = self.curs.fetchall()
        for data in result:
            list.append(data["performance_id"])

        return list

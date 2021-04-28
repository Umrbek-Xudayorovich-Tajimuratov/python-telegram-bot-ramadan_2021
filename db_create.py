from sqlite3 import connect, Row


class DBHelper:
    def __init__(self, db_name):
        self.conn = connect(db_name, check_same_thread=False)
        self.conn.row_factory = Row
        self.cursor = self.conn.cursor()

    def get_regions(self):
        return self.cursor.execute(
            """
            SELECT region_id, regions FROM reggs ORDER BY region_id LIMIT 20
            """
        ).fetchall()

    def get_region(self, opted_region_id):
        return self.cursor.execute(
            """
            SELECT  region_id, regions FROM reggs WHERE region_id=?
            """, (opted_region_id,)
        ).fetchone()

    def get_calendar_by_region(self, opted_region_id, dt):
        return self.cursor.execute(
            """
            SELECT * FROM ram_cal WHERE date=? and region_id=?
            """
            , (dt, opted_region_id)
        ).fetchone()

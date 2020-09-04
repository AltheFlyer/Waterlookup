import sqlite3


class CourseDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def lookup(self, searchby: str):
        t = (searchby,)
        self.cursor.execute("""
            SELECT * 
            FROM courses
            WHERE searchby=?;
        """, t)
        return self.cursor.fetchone()

    def lookup_partial(self, searchby: str):
        t = (searchby + "%",)
        self.cursor.execute("""
            SELECT *
            FROM courses
            WHERE searchby LIKE ?;
        """, t)
        return self.cursor.fetchall()

    def lookup_subject(self, searchby: str):
        t = (searchby,)
        self.cursor.execute("""
            SELECT *
            FROM courses
            WHERE subject=?;
        """, t)
        return self.cursor.fetchall()
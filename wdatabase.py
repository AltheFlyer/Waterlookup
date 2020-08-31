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
            WHERE searchby=? 
        """, t)
        return self.cursor.fetchone()
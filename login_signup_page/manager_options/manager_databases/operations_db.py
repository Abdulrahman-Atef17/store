import sqlite3

class Operations:
    def __init__(self, operations_db):
        self.con = sqlite3.connect(operations_db)
        self.cur = self.con.cursor()
        sql = '''
            CREATE TABLE IF NOT EXISTS operations(
            date text,
            type text,
            source text,
            quantity text,
            id INTEGER PRIMARY KEY AUTOINCREMENT
            )'''
        self.cur.execute(sql)
        self.con.commit()

    def insert_operation(self, type, source, quantity):
        self.cur.execute('insert into operations(date, type, source, quantity) values(Date("now"), ?, ?, ?)', (type, source, quantity))
        self.con.commit()

    def fetch_operations(self):
        self.cur.execute('select * from operations')
        rows = self.cur.fetchall()
        return rows

    def fetch_last_operation(self):
        row = self.cur.execute('SELECT id FROM operations ORDER BY id DESC LIMIT 1').fetchone()
        return row

    def remove_operation(self, id):
        self.cur.execute('delete from operations where id=?', [id])
        self.cur.execute('delete from sqlite_sequence where name="operations"')
        self.cur.execute('update operations set id=id-1 where ?<id', [id])
        self.con.commit()
import sqlite3

class ExpensesDatabase:
    def __init__(self, expenses_db):
        self.con = sqlite3.connect(expenses_db)
        self.cur = self.con.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS expenses(
        date text,
        cause text,
        quantity text,
        operation_no text NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        ''' 
        self.cur.execute(sql)
        self.con.commit()

    def insert_expenses(self, cause, quantity, operation_no):
        self.cur.execute('insert into expenses values(DATE("now"), ?, ?, ?, NULL)', (cause, quantity, operation_no))
        self.con.commit()

    def fetch_expenses(self):
        rows = self.cur.execute('select * from expenses').fetchall()
        return rows
    
    def fetch_operation_no(self, id):
        row = self.cur.execute('select operation_no from expenses where id=?', [id]).fetchone()
        return row

    def remove_expenses(self, id):
        self.cur.execute('delete from expenses where id=?', [id])
        self.cur.execute('delete from sqlite_sequence where name="expenses"')
        self.cur.execute('update expenses set id=id-1 where ?<id', [id])
        self.con.commit()
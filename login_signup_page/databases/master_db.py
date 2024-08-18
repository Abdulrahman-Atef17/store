import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = '''
            CREATE TABLE IF NOT EXISTS master(
            username text,
            password text
            )
        '''
        self.cur.execute(sql)
        self.con.commit()
    
    def insert(self, username, password):
        self.cur.execute('insert into master values (?,?)', (username, password))
        self.con.commit()
        return username, password

    def fetch(self):
        rows = self.cur.execute("SELECT * FROM master LIMIT 1").fetchall()
        return rows
    
    def check(self, username, password):
        self.cur.execute('select * from master where username=? and password=?', (username, password))
        rows = self.cur.fetchall()
        return rows
    
    def check_pass(self, password):
        self.cur.execute('select password from master where password=?', [password])
        rows = self.cur.fetchall()
        return rows
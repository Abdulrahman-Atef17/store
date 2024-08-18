import sqlite3

class ManagersDatabase:
    def __init__(self, man_db):
        self.con = sqlite3.connect(man_db)
        self.cur = self.con.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS managers(
        man_username text,
        man_password text
        )'''
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, man_username, man_password):
        self.cur.execute('insert into managers values(?,?)', (man_username, man_password))
        self.con.commit()

    def check(self, login_username, login_password):
        self.cur.execute('select * from managers where man_username=? and man_password=?', (login_username, login_password))
        rows = self.cur.fetchall()
        return rows
        

    def check_exist(self, man_username):
        self.cur.execute('select * from managers where man_username=?', [man_username])
        rows = self.cur.fetchall()
        return rows
    
    def check_pass(self, man_password):
        self.cur.execute('select man_password from managers where man_password=?', [man_password])
        rows = self.cur.fetchall()
        return rows
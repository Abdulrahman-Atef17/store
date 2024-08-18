import sqlite3

class EmployeesDatabase:
    def __init__(self, emp_db):
        self.con = sqlite3.connect(emp_db)
        self.cur = self.con.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS employees(
        emp_username text,
        emp_password text
        )'''
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, emp_username, emp_password):
        self.cur.execute('insert into employees values(?,?)', (emp_username, emp_password))
        self.con.commit()

    def check(self, login_username, login_password):
        self.cur.execute('select * from employees where emp_username=? and emp_password=?', (login_username, login_password))
        rows = self.cur.fetchall()
        return rows
    
    def check_exist(self, emp_username):
        self.cur.execute('select * from employees where emp_username=?', [emp_username])
        rows = self.cur.fetchall()
        return rows
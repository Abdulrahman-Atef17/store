import sqlite3

class CustomersDatabase:
    def __init__(self, customers_db):
        self.con = sqlite3.connect(customers_db)
        self.cur = self.con.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS customers(
        type text,
        address text,
        phone_no text,
        name text,
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        '''
        self.cur.execute(sql)
        self.con.commit()

    def insert_customer(self, type, address, phone_no, name):
        self.cur.execute('insert into customers(type, address, phone_no, name) values(?, ?, ?, ?)', (type, address, phone_no, name))
        self.con.commit()

    def fetch_customers(self):
        rows = self.cur.execute('select * from customers').fetchall()
        return rows

    def update_customer(self, type, address, phone_no, name, id):
        self.cur.execute('update customers set type=?, address=?, phone_no=?, name=? where id=?', (type, address, phone_no, name, id))
        self.con.commit()

    def check_existence(self, name, id):
        rows = self.cur.execute('select * from customers where name=? and id=?', (name,id)).fetchall()
        return rows

    def check_existence1(self, name):
        rows = self.cur.execute('select * from customers where name=?', (name,)).fetchall()
        return rows

    def search_id(self, id):
        self.cur.execute("SELECT * FROM customers WHERE INSTR(id, ?)", (id,))
        rows = self.cur.fetchall()
        return rows

    def search_name(self, name):
        self.cur.execute("SELECT * FROM customers WHERE INSTR(name, ?)", (name,))
        rows = self.cur.fetchall()
        return rows

    def search_address(self, address):
        self.cur.execute("SELECT * FROM customers WHERE INSTR(address, ?)", (address,))
        rows = self.cur.fetchall()
        return rows
    
    def search_type(self, type):
        self.cur.execute("SELECT * FROM customers WHERE INSTR(type, ?)", (type,))
        rows = self.cur.fetchall()
        return rows

    def remove_customer(self, id):
        self.cur.execute('delete from customers where id=?', (id,))
        self.cur.execute('delete from sqlite_sequence where name="customers"')
        self.cur.execute('update customers set id=id-1 where ?<id', (id,))
        self.con.commit()
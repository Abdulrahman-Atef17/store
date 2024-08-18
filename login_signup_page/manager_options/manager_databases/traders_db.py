import sqlite3

class TradersDatabase:
    def __init__(self, traders_db):
        self.con = sqlite3.connect(traders_db)
        self.cur = self.con.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS traders(
        address text,
        phone_no text,
        name text,
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        '''
        self.cur.execute(sql)
        self.con.commit()

    def insert_trader(self, address, phone_no, name):
        self.cur.execute('insert into traders(address, phone_no, name) values(?, ?, ?)', (address, phone_no, name))
        self.con.commit()

    def fetch_traders(self):
        rows = self.cur.execute('select * from traders').fetchall()
        return rows

    def update_trader(self, address, phone_no, name, id):
        self.cur.execute('update traders set address=?, phone_no=?, name=? where id=?', (address, phone_no, name, id))
        self.con.commit()

    def check_existence(self, name, id):
        rows = self.cur.execute('select * from traders where name=? and id!=?', (name,id)).fetchall()
        return rows
    
    def check_existence1(self, name):
        rows = self.cur.execute('select * from traders where name=?', (name,)).fetchall()
        return rows
    
    def search_id(self, id):
        self.cur.execute("SELECT * FROM traders WHERE INSTR(id, ?)", (id,))
        rows = self.cur.fetchall()
        return rows

    def search_name(self, name):
        self.cur.execute("SELECT * FROM traders WHERE INSTR(name, ?)", (name,))
        rows = self.cur.fetchall()
        return rows

    def search_address(self, address):
        self.cur.execute("SELECT * FROM traders WHERE INSTR(address, ?)", (address,))
        rows = self.cur.fetchall()
        return rows

    def remove_trader(self, id):
        self.cur.execute('delete from traders where id=?', (id,))
        self.cur.execute('delete from sqlite_sequence where name="traders"')
        self.cur.execute('update traders set id=id-1 where ?<id', (id,))
        self.con.commit()
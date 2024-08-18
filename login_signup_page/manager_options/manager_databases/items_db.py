import sqlite3

class ItemsDatabase:
    def __init__(self, items_db):
        self.con = sqlite3.connect(items_db)
        self.cur = self.con.cursor()

        sql = '''
        CREATE TABLE IF NOT EXISTS items(
            item_name text,
            id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        '''

        self.cur.execute(sql)
        self.con.commit()

    def insert(self, item_name):
        self.cur.execute('insert into items values(?,NULL)', [item_name])
        self.con.commit()

    def fetch(self):
        self.cur.execute('select * from items')
        rows = self.cur.fetchall()
        return rows
    
    def update(self, id, item_name):
        self.cur.execute('update items set item_name=? where id=?', (id, item_name))
        self.con.commit()

    def remove(self, id):
        self.cur.execute('delete from items where id=?', (id,))
        self.cur.execute('delete from sqlite_sequence where name="items"')
        self.cur.execute('update items set id=id-1')
        self.con.commit()

    def check_existence(self, item_name):
        self.cur.execute('select * from items where item_name=?', [item_name])
        rows = self.cur.fetchall()
        return rows
    
    def fetch_name(self):
        self.cur.execute('select DISTINCT(item_name) as item_name from items')
        rows = self.cur.fetchall()
        return rows
import sqlite3

class ProductsDatabase:
    def __init__(self, pro_db):
        self.con = sqlite3.connect(pro_db)
        self.cur = self.con.cursor()

        sql= '''
        CREATE TABLE IF NOT EXISTS products(
        date_of_buy text,
        item text,
        trader text,
        sell_price text,
        low_sell_price text,
        buy_price text,
        count text,
        name text,
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
'''
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, date_of_buy, item, trader, sell_price, low_sell_price, buy_price, count, name):
        self.cur.execute('INSERT into products values(?,?,?,?,?,?,?,?,NULL)',
                        (date_of_buy, item, trader, sell_price, low_sell_price, buy_price, count, name))
        self.con.commit()

    def fetch(self):
        self.cur.execute('SELECT * FROM products')
        rows = self.cur.fetchall()
        return rows

    def update(self, date_of_buy, item, trader, sell_price, low_sell_price, buy_price, count, name, id):
        self.cur.execute('update products set date_of_buy=?,item=?,trader=?,sell_price=?,low_sell_price=?,buy_price=?,count=?,name=? where id=?',
                        (date_of_buy, item, trader, sell_price, low_sell_price, buy_price, count, name, id))
        self.con.commit()

    def upadte_items(self, old, new):
        self.cur.execute('update products set item=? where item=?',
                        (new, old))
        self.con.commit()

    def update_prices_count(self, count, buy_price, low_Sell_price, sell_price, id):
        self.cur.execute('update products set date_of_buy=DATE("now"), count=count+?, buy_price=?, low_sell_price=?, sell_price=? where id=?', (count, buy_price, low_Sell_price, sell_price, id))
        self.con.commit()

    def decrease_count(self, sold, id):
        self.cur.execute('update products set count=count-? where id=?', (sold, id))
        self.con.commit()
    
    def increase_count(self, sold, id):
        self.cur.execute('update products set count=count+? where id=?', (sold, id))
        self.con.commit()

    def update_product_trader(self, new, old):
        self.cur.execute('update products set trader=? where trader=?', (new, old))
        self.con.commit()

    def remove(self, selected_id):
        self.cur.execute('delete from products where id=?', (selected_id,))
        self.cur.execute('delete from sqlite_sequence where name="products"')
        self.cur.execute('update products set id=id-1 where ?<id', (selected_id,))
        self.con.commit()

    def search_id(self, id):
        self.cur.execute('select * from products where id=?', (id,))
        rows = self.cur.fetchall()
        return rows
    
    def search_item(self, item):
        self.cur.execute("SELECT * FROM products WHERE INSTR(item, ?)", (item,))
        rows = self.cur.fetchall()
        return rows
    
    def search_name(self, name):
        self.cur.execute("SELECT * FROM products WHERE INSTR(name, ?)", (name,))
        rows = self.cur.fetchall()
        return rows
    
    def search_trader(self, trader):
        self.cur.execute('select * from products where instr(trader, ?)', (trader,))
        rows = self.cur.fetchall()
        return rows
    
    def id_product_to_bill(self, id):
        self.cur.execute('select id,name,sell_price,low_sell_price,buy_price from products where id=?', [id])
        rows = self.cur.fetchall()
        return rows
    
    def name_product_to_bill(self, name):
        self.cur.execute('select id, name, sell_price, low_sell_price, buy_price from products where name=?', (name,))
        rows = self.cur.fetchall()
        return rows
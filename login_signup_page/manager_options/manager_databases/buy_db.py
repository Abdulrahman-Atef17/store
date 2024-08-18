import sqlite3

class buyDatabase:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS buy_bills (
                date text,
                change text,
                total TEXT,
                trader TEXT,
                bill_no INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            );
        ''')

        self.cur.execute('PRAGMA foreign_keys = ON')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS buy_bill (
                total_price TEXT,
                product_buy_price TEXT,
                count INTEGER,
                product_name TEXT,
                product_code INTEGER,
                bill_no INTEGER NOT NULL,
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (bill_no) REFERENCES buy_bills(bill_no)
            );
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS payments(
                date text,
                quantity text,
                operation_no text,
                bill_no INTEGER NOT NULL,
                payment_no INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (bill_no) REFERENCES buy_bills(bill_no)
            )
        ''')
        self.con.commit()

    def insert_bill(self, change, total, trader):
        self.cur.execute('''
            INSERT INTO buy_bills (date, change, total, trader) 
            VALUES (Date('now'), ?, ?, ?)
        ''', (change, total, trader))
        self.con.commit()

    def insert_product(self, total_price, product_buy_price, count, product_name, product_code, bill_no):
        self.cur.execute('''
            INSERT INTO buy_bill VALUES (?, ?, ?, ?, ?, ?, NULL)
        ''', (total_price, product_buy_price, count, product_name, product_code, bill_no))
        self.con.commit()

    def insert_payment(self, quantity, operation_no, bill_no):
        self.cur.execute('insert into payments values(Date("now"), ?, ?, ?, NULL)', (quantity, operation_no, bill_no))
        self.con.commit()

    def fetch_bills(self):
        rows = self.cur.execute('SELECT * FROM buy_bills').fetchall()
        return rows

    def fetch_last_bill_no(self):
        self.cur.execute('SELECT bill_no FROM buy_bills ORDER BY bill_no DESC LIMIT 1')
        rows = self.cur.fetchone()
        return rows[0] if rows else None

    def fetch_bills_trader(self, trader):
        rows = self.cur.execute('select * from buy_bills where trader=?', (trader,)).fetchall()
        return rows

    def fetch_products(self, bill_no):
        rows = self.cur.execute('''
        SELECT bb.total_price, bb.product_buy_price, bb.count, bb.product_name, bb.product_code, bb.bill_no
        FROM buy_bill bb
        INNER JOIN buy_bills bbs ON bb.bill_no = bbs.bill_no
        WHERE bb.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows

    def fetch_products_info(self, bill_no):
        rows = self.cur.execute('''
        SELECT bb.total_price, bb.product_buy_price, bb.count
        FROM buy_bill bb
        INNER JOIN buy_bills bbs ON bb.bill_no = bbs.bill_no
        WHERE bb.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows

    def fetch_product_total(self, bill_no):
        rows = self.cur.execute('''
        SELECT bb.total_price, bb.product_buy_price, bb.count, bb.product_name, bb.product_code 
        FROM buy_bill bb
        INNER JOIN buy_bills bbs ON bb.bill_no = bbs.bill_no,
        where bill_no=?
        ''', (bill_no,)).fetchall()
        return rows

    def fetch_payments(self, bill_no):
        rows = self.cur.execute('''
        SELECT p.date, p.quantity, p.operation_no, p.payment_no
        FROM payments p
        INNER JOIN buy_bills bbs ON p.bill_no = bbs.bill_no
        WHERE p.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows

    def fetch_operation_no(self, payment_no):
        row = self.cur.execute('select operation_no from payments where payment_no=?', (payment_no,)).fetchone()
        return row

    def fetch_operation_no1(self, bill_no):
        row = self.cur.execute('select operation_no from payments where bill_no=?', (bill_no,)).fetchall()
        return row

    def update_bill(self, trader, bill_no):
        self.cur.execute('update buy_bills set trader=? where bill_no=?', (trader, bill_no))
        self.con.commit()

    def update_bill_total_change(self, total, change, bill_no):
        self.cur.execute('update buy_bills set change=?, total=? where bill_no=?', (change, total, bill_no,))
        self.con.commit()

    def update_bill_trader(self, new, old):
        self.cur.execute('update buy_bills set trader=? where trader=?', (new, old))
        self.con.commit()

    def update_product(self, total_price, product_buy_price, count, product_code):
        self.cur.execute('''update buy_bill set total_price=?, product_buy_price=?, count=? where product_code=?''',
                        (total_price, product_buy_price, count, product_code))
        self.con.commit()

    def search_bill_no(self, bill_no):
        self.cur.execute("SELECT * FROM buy_bills WHERE bill_no=?", (bill_no,))
        rows = self.cur.fetchall()
        return rows
    
    def search_trader_bill_no(self, bill_no, trader):
        self.cur.execute("SELECT * FROM buy_bills WHERE bill_no=?and trader=?", (bill_no,trader))
        rows = self.cur.fetchall()
        return rows

    def search_trader(self, trader):
        self.cur.execute("SELECT * FROM buy_bills WHERE INSTR(trader, ?)", (trader,))
        rows = self.cur.fetchall()
        return rows

    def search_date(self, date, trader):
        self.cur.execute("SELECT * FROM buy_bills WHERE INSTR(date, ?) and trader=?", (date,trader))
        rows = self.cur.fetchall()
        return rows
    
    def search_trader_date(self, date):
        self.cur.execute("SELECT * FROM buy_bills WHERE INSTR(date, ?)", (date,))
        rows = self.cur.fetchall()
        return rows

    def remove_bill(self, bill_no):
        self.cur.execute('delete from payments where bill_no=?', (bill_no,))
        self.cur.execute('delete from buy_bill where bill_no=?', (bill_no,))
        self.cur.execute('delete from buy_bills where bill_no=?', (bill_no,))
        self.cur.execute('delete from sqlite_sequence where name="buy_bills"')
        self.cur.execute('update buy_bills set bill_no=bill_no-1 where ?<bill_no', (bill_no,))
        self.con.commit()

    def remove_product(self, id):
        self.cur.execute('delete from buy_bill where id=?', (id))
        self.cur.execute('delete from sqlite_sequence where name="buy_bill"')
        self.cur.execute('update buy_bill set id=id-1 where ?<id', [id])
        self.con.commit()

    def remove_payment(self, payment_no):
        self.cur.execute('delete from payments where payment_no=?', [payment_no])
        self.cur.execute('delete from sqlite_sequence where name="payments"')
        self.cur.execute('update payments set payment_no=payment_no-1 where ?<payment_no', [payment_no])
        self.con.commit()

    def close(self):
        if self.con:
            self.con.close()
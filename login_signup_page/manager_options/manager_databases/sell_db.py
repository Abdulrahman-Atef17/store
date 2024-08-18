import sqlite3

class SellDatabase:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS sell_bills (
                type TEXT,
                change text,
                total TEXT,
                customer_name TEXT,
                bill_no INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            );
        ''')

        self.cur.execute('PRAGMA foreign_keys = ON')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS sell_bill (
                total_profit TEXT,
                total_price TEXT,
                product_buy_price TEXT,
                product_low_sell_price text,
                product_sell_price TEXT,
                count INTEGER,
                product_name TEXT,
                product_code INTEGER,
                bill_no INTEGER NOT NULL,
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (bill_no) REFERENCES sell_bills(bill_no) ON DELETE CASCADE
            );
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS payments(
                date text,
                quantity text,
                payer text,
                operation_no text,
                bill_no INTEGER NOT NULL,
                payment_no INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (bill_no) REFERENCES sell_bills(bill_no) ON DELETE CASCADE
            )
        ''')
        self.con.commit()

    def insert_bill(self, type, change, total, customer_name):
        self.cur.execute('''
            INSERT INTO sell_bills (type, change, total, customer_name) 
            VALUES (?, ?, ?, ?)
        ''', (type, change, total, customer_name))
        self.con.commit()

    def insert_product(self, total_profit, total_price, product_buy_price, product_low_sell_price, product_sell_price, count, product_name, product_code, bill_no):
        self.cur.execute('''
            INSERT INTO sell_bill VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
        ''', (total_profit, total_price, product_buy_price, product_low_sell_price, product_sell_price, count, product_name, product_code, bill_no))
        self.con.commit()

    def insert_payment(self, payer, quantity, operation_no, bill_no):
        self.cur.execute('insert into payments values(Date("now"), ?, ?, ?, ?, NULL)', (payer, quantity, operation_no, bill_no))
        self.con.commit()

    def fetch_bills(self):
        rows = self.cur.execute('SELECT * FROM sell_bills').fetchall()
        return rows

    def fetch_bills_customer(self, customer):
        rows = self.cur.execute('select * from sell_bills where customer_name=?', (customer,)).fetchall()
        return rows

    def fetch_last_bill_no(self):
        self.cur.execute('SELECT bill_no FROM sell_bills ORDER BY bill_no DESC LIMIT 1')
        rows = self.cur.fetchone()
        return rows[0] if rows else None
    
    def fetch_products(self, bill_no):
        rows = self.cur.execute('''
        SELECT sb.total_price, sb.product_buy_price, sb.product_low_sell_price, sb.product_sell_price, sb.count, sb.product_name, sb.product_code, sb.bill_no
        FROM sell_bill sb
        INNER JOIN sell_bills sbs ON sb.bill_no = sbs.bill_no
        WHERE sb.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows

    def fetch_products_info(self, bill_no):
        rows = self.cur.execute('''
        SELECT sb.total_price, sb.product_sell_price, sb.count
        FROM sell_bill sb
        INNER JOIN sell_bills sbs ON sb.bill_no = sbs.bill_no
        WHERE sb.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows
    
    def fetch_product_total(self, bill_no):
        rows = self.cur.execute('''
        SELECT sb.total_price, sb.product_low_sell_price, sb.product_sell_price, sb.count, sb.product_name, sb.product_code 
        FROM sell_bill sb
        INNER JOIN sell_bills sbs ON sb.bill_no = sbs.bill_no,
        where bill_no=?
        ''', (bill_no,)).fetchall()
        return rows
    
    def fetch_payments(self, bill_no):
        rows = self.cur.execute('''
        SELECT p.date, p.payer, p.quantity, p.operation_no, p.payment_no
        FROM payments p
        INNER JOIN sell_bills sbs ON p.bill_no = sbs.bill_no
        WHERE p.bill_no = ?
        ''', (bill_no,)).fetchall()
        return rows
    
    def fetch_operation_no(self, payment_no):
        row = self.cur.execute('select operation_no from payments where payment_no=?', (payment_no,)).fetchone()
        return row

    def fetch_operation_no1(self, bill_no):
        row = self.cur.execute('select operation_no from payments where bill_no=?', (bill_no,)).fetchall()
        return row

    def update_bill(self, customer_name, bill_no):
        self.cur.execute('update sell_bills set customer_name=? where bill_no=?', (customer_name, bill_no))
        self.con.commit()

    def update_bill_total_change(self, total, change, bill_no):
        self.cur.execute('update sell_bills set change=?, total=? where bill_no=?', (change, total, bill_no,))
        self.con.commit()

    def update_bill_customer(self, new, old):
        self.cur.execute('update sell_bills set customer_name=? where customer_name=?', (new, old))
        self.con.commit()

    def update_product(self, total_profit, total_price, product_low_sell_price, product_sell_price, count, product_code):
        self.cur.execute('''update sell_bill set total_profit=?, total_price=?, product_low_sell_price=?, product_sell_price=?, count=? where product_code=?''',
                        (total_profit, total_price, product_low_sell_price, product_sell_price, count, product_code))
        self.con.commit()

    def search_type(self, type):
        self.cur.execute("SELECT * FROM sell_bills WHERE INSTR(type, ?)", (type,))
        rows = self.cur.fetchall()
        return rows
    
    def search_bill_no(self, bill_no):
        self.cur.execute("SELECT * FROM sell_bills WHERE INSTR(bill_no, ?)", (bill_no,))
        rows = self.cur.fetchall()
        return rows
    
    def search_customer_name(self, customer_name):
        self.cur.execute("SELECT * FROM sell_bills WHERE INSTR(customer_name, ?)", (customer_name,))
        rows = self.cur.fetchall()
        return rows

    def search_customer_bill_no(self, bill_no, trader):
        self.cur.execute("SELECT * FROM buy_bills WHERE bill_no=?and trader=?", (bill_no,trader))
        rows = self.cur.fetchall()
        return rows

    def search_customer_date(self, date):
        self.cur.execute("SELECT * FROM buy_bills WHERE INSTR(date, ?)", (date,))
        rows = self.cur.fetchall()
        return rows

    def remove_bill(self, bill_no):
        self.cur.execute('delete from payments where bill_no=?', [bill_no])
        self.cur.execute('delete from sell_bill where bill_no=?', [bill_no])
        self.cur.execute('delete from sell_bills where bill_no=?', [bill_no])
        self.cur.execute('delete from sqlite_sequence where name="sell_bills"')
        self.cur.execute('update sell_bills set bill_no=bill_no-1 where ?<bill_no', (bill_no,))

        self.con.commit()

    def remove_product(self, id):
        self.cur.execute('delete from sell_bill where product_code=?', (id))
        self.cur.execute('delete from sqlite_sequence where name="sell_bill"')
        self.cur.execute('update sell_bill set id=id-1')
        self.con.commit()

    def remove_payment(self, payment_no):
        self.cur.execute('delete from payments where payment_no=?', [payment_no])
        self.cur.execute('delete from sqlite_sequence where name="payments"')
        self.cur.execute('update payments set payment_no=payment_no-1 where ?<payment_no', [payment_no])
        self.con.commit()

    def close(self):
        if self.con:
            self.con.close()
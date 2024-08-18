from tkinter import *
from subprocess import Popen
from databases.master_db import Database
from databases.managers_db import ManagersDatabase
from databases.employees_db import EmployeesDatabase

root = Tk()

width = int(root.winfo_screenwidth())
height = int(root.winfo_screenheight())
root.state('zoomed')
root.title('Company Name')
root.config(bg='#ABB2B9')


#---------------------------- variables -----------------------------
items_img = PhotoImage(file='images\\sections\\items.png')
products_img = PhotoImage(file='images\\sections\\products.png')
selling_bill_img = PhotoImage(file='images\\sections\\selling_bill.png')
buying_bill_img = PhotoImage(file='images\\sections\\buying_bill.png')
money_lock_img = PhotoImage(file='images\\sections\\money_lock.png')
expenses_img = PhotoImage(file='images\\sections\\expenses.png')
customers_img = PhotoImage(file='images\\sections\\customers.png')
traders_img = PhotoImage(file='images\\sections\\traders.png')
storage_img = PhotoImage(file='images\\sections\\storage.png')
reports_img = PhotoImage(file='images\\sections\\reports.png')
settings_img = PhotoImage(file='images\\sections\\settings.png')
calculator_img = PhotoImage(file='images\\sections\\calculator.png')

products_path = 'login_signup_page\\manager_options\\products.py'
items_path = 'login_signup_page\\manager_options\\items.py'
sell_path = 'login_signup_page\\manager_options\\sell.py'
buy_path = 'login_signup_page\\manager_options\\buy.py'
money_path = 'login_signup_page\\manager_options\\money.py'
expenses_path = 'login_signup_page\\manager_options\\expenses.py'
traders_path = 'login_signup_page\\manager_options\\traders.py'
customers_path = 'login_signup_page\\manager_options\\customers.py'
#---------------------------- Functions -----------------------------
def products_page():
    Popen(['python', products_path])
    quit()

def items_page():
    Popen(['python', items_path])
    quit()

def sell_page():
    Popen(['python', sell_path])
    quit()

def buy_page():
    Popen(['python', buy_path])
    quit()

def money_page():
    Popen(['python', money_path])
    quit()

def expenses_page():
    Popen(['python', expenses_path])
    quit()

def traders_page():
    Popen(['python', traders_path])
    quit()

def customers_page():
    Popen(['python', customers_path])
    quit()

def options2():
    customers_btn = Button(root, text='العملاء', image=customers_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=customers_page)
    customers_btn.place(x=width*.1, y=height*.02, width=width*.2, height=height*.2)
    traders_btn = Button(root, text='الموردون', image=traders_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=traders_page)
    traders_btn.place(x=width*.7, y=height*.02, width=width*.2, height=height*.2)
    reports_btn = Button(root, text='تقارير نهائية', image=reports_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2')
    reports_btn.place(x=width*.1, y=height*.32, width=width*.2, height=height*.2)
    storage_btn = Button(root, text='تقارير المخزن', image=storage_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2')
    storage_btn.place(x=width*.7, y=height*.32, width=width*.2, height=height*.2)
    calculator_btn = Button(root, text='الآلة الحاسبة', image=calculator_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2')
    calculator_btn.place(x=width*.1, y=height*.62, width=width*.2, height=height*.2)
    settings_btn = Button(root, text='الإعدادات', image=settings_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2')
    settings_btn.place(x=width*.7, y=height*.62, width=width*.2, height=height*.2)

def options1():
    products_btn = Button(root, text='المنتجات', image=products_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=products_page)
    products_btn.place(x=width*.7, y=height*.02, width=width*.2, height=height*.2)
    items_btn = Button(root, text='الأصناف', image=items_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=items_page)
    items_btn.place(x=width*.1, y=height*.02, width=width*.2, height=height*.2)
    sales_btn = Button(root, text='المشتريات', image=buying_bill_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=buy_page)
    sales_btn.place(x=width*.1, y=height*.32, width=width*.2, height=height*.2)
    buys_btn = Button(root, text='المبيعات', image=selling_bill_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=sell_page)
    buys_btn.place(x=width*.7, y=height*.32, width=width*.2, height=height*.2)
    money_btn = Button(root, text='المصروفات', image=expenses_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=expenses_page)
    money_btn.place(x=width*.1, y=height*.62, width=width*.2, height=height*.2)
    expenses_btn = Button(root, text='الصندوق', image=money_lock_img, compound=TOP, fg='#117A65', bg='#ABB2B9', font=('tajawal', 12, 'bold'), cursor='hand2', command=money_page)
    expenses_btn.place(x=width*.7, y=height*.62, width=width*.2, height=height*.2)

options1()
round_button = PhotoImage(file='images\\options_button.png')
options1_btn = Button(root, image=round_button, bd=0, bg='#ABB2B9', cursor='hand2', command=options2)
options1_btn.place(x=width*.48, y=height*.9, width=10, height=10)

options2_btn = Button(root, image=round_button, bd=0, bg='#ABB2B9', cursor='hand2', command=options1)
options2_btn.place(x=width*.52, y=height*.9, width=10, height=10)

root.mainloop()
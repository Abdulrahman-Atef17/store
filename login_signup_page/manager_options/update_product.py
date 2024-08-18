from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from subprocess import Popen
from manager_databases.products_db import ProductsDatabase
from manager_databases.items_db import ItemsDatabase
import json
import os

root = Tk()
width = int(root.winfo_screenwidth())
height = int(root.winfo_screenheight())
root.state('zoomed')
root.title('Company Name')
root.config(bg='#ABB2B9')


#--------------------------- Vraiables -------------------------
pro_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')
items_db = ItemsDatabase('login_signup_page\\manager_options\\manager_databases\\items_db.db')
back_icon = PhotoImage(file='images\\left_arrow.png')

global name, count, buy_price, low_sell_price, sell_price, trader, date_of_buy
id = IntVar()
name = StringVar()
count = StringVar()
buy_price = StringVar()
low_sell_price = StringVar()
sell_price = StringVar()
trader = StringVar()
item = StringVar()
date_of_buy = StringVar()


#--------------------------- Functions ------------------------------
def load():
    with open('data_file.json', 'r') as rf:
        global data, got_date, got_item, got_trader, got_sell_price, got_low_sell_price, got_buy_price, got_count, got_name, got_id
        data = json.load(rf)
    if os.path.getsize('data_file.json') > 2:
        got_date, got_item, got_trader, got_sell_price, got_low_sell_price, got_buy_price, got_count, got_name, got_id = data
        date_of_buy.set(got_date)
        item.set(got_item)
        trader.set(got_trader)
        sell_price.set(got_sell_price)
        low_sell_price.set(got_low_sell_price)
        buy_price.set(got_buy_price)
        count.set(got_count)
        name.set(got_name)
        return date_of_buy, item, trader, sell_price, low_sell_price, buy_price, count, name, got_id
load()

def delete():
    pro_db.remove(got_id)
    with open('data_file.json', 'w') as wf:
        json.dump("", wf)
    Popen(['python', 'login_signup_page\\manager_options\\products.py'])
    quit()


def update():
    if name_entry.get() == '' or count_entry.get() == '' or buy_price_entry.get() == '' or low_sell_price_entry.get() == '' or sell_price_entry.get() == '' or trader_entry.get() == '':
        messagebox.showerror('Error', 'All Fields must be filled')
    pro_db.update(
        date_of_buy.set(date_of_buy_entry.get()),
        item.set(item_entry.get()),
        trader.set(trader_entry.get()),
        sell_price.set(sell_price_entry.get()),
        low_sell_price.set(low_sell_price_entry.get()),
        buy_price.set(buy_price_entry.get()),
        count.set(count_entry.get()),
        name.set(name_entry.get()),
        got_id
        )
    return (date_of_buy_entry.get(), item_entry.get(), trader_entry.get(), sell_price_entry.get(), low_sell_price_entry.get(), buy_price_entry.get(), count_entry.get(), name_entry.get(), got_id)

def save1():
    data = update()
    with open('data_file.json', 'w') as wf:
        json.dump(data, wf)
    messagebox.showinfo('Success', 'Infromation was updated!')
    Popen(['python', 'login_signup_page\\manager_options\\products.py'])
    quit()
        
def go_back():
    Popen(['python', 'login_signup_page\\manager_options\\products.py'])
    quit()


#----------------------- Upside Frame -------------------------------
upside_frame = Frame(root, bg='#117A65')
upside_frame_height = 35
upside_frame_width = width
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='تعديل بيانات المنتج', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo_img = PhotoImage(file='images\\logos\\products.png')
logo = Label(upside_frame, image=logo_img, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.005, y=upside_frame_height*.15)


#---------------------- Main Frame ---------------------------------------
name_lb = Label(root, text='اسم المنتج *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), justify=RIGHT)
name_lb.place(x=width*.93, y=height * .08)
global name_entry
name_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=name)
name_entry.place(x=width*.595, y=height*.13, width=width*.4)

count_lb = Label(root, text='عدد القطع *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
count_lb.place(x=width*.94, y=height*.20)
global count_entry
count_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=count)
count_entry.place(x=width*.808, y=height*.20, width=width*.1)

buy_price_lb = Label(root, text='سعر الشراء *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), )
buy_price_lb.place(x=width*.935, y=height*.28)
global buy_price_entry
buy_price_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=buy_price)
buy_price_entry.place(x=width*.808, y=height*.28, width=width*.1)

low_sell_price_lb = Label(root, text='سعر البيع جملة *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), )
low_sell_price_lb.place(x=width*.92, y=height*.36)
global low_sell_price_entry
low_sell_price_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=low_sell_price)
low_sell_price_entry.place(x=width*.808, y=height*.36, width=width*.1)

sell_price_lb = Label(root, text='سعر البيع قطاعي *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), )
sell_price_lb.place(x=width*.91, y=height*.44)
global sell_price_entry
sell_price_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=sell_price)
sell_price_entry.place(x=width*.808, y=height*.44, width=width*.1)

trader_lb = Label(root, text='المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), )
trader_lb.place(x=width*.96, y=height*.52)
global trader_entry
trader_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=trader)
trader_entry.place(x=width*.808, y=height*.52, width=width*.1)

options = []
list = list(items_db.fetch_name())
for row in list:
    options.append(row[0])
item_lb = Label(root, text='الصنف', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), )
item_lb.place(x=width*.96, y=height*.6)
global item_entry
item_entry = ttk.Combobox(root, font=('tajawal', 12, 'bold'), justify=CENTER, state='readonly', values=options, textvariable=item)
item_entry.place(x=width*.808, y=height*.6, width=width*.1)

date_of_buy_lb = Label(root, text='تاريخ الشراء *', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
date_of_buy_lb.place(x=width*.935, y=height*.68)
global date_of_buy_entry
date_of_buy_entry = Entry(root, fg='#117A65', font=('tajawal', 12, 'bold'), justify=CENTER, bd=0, highlightthickness=2, highlightbackground='#117A65', textvariable=date_of_buy)
date_of_buy_entry.place(x=width*.808, y=height*.68, width=width*.1)

save_btn = Button(root, text='تعديل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief='solid', cursor='hand2', command=save1)
save_btn.place(x=width*.6, y=height*.85, width=width*.1)
cancel_btn = Button(root, text='حذف', bg='#ABB2B9', fg='red', font=('tajawal', 12, 'bold'), bd=2, relief='solid', cursor='hand2', command=delete)
cancel_btn.place(x=width*.4, y=height*.85, width=width*.1)

root.mainloop()
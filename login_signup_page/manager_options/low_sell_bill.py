from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen
import json
import os
from datetime import date
from PIL import Image, ImageTk
from manager_databases.products_db import ProductsDatabase
from manager_databases.sell_db import SellDatabase
from manager_databases.operations_db import Operations

root = Tk()
root.state('zoomed')
root.title('Company Name')

#---------------- Variables ----------------------
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

sell_logo = PhotoImage(file='images\\logos\\selling_bill.png')
back_icon = PhotoImage(file='images\\left_arrow.png')
add_icon = PhotoImage(file='images\\add_icon.png')
save_icon = PhotoImage(file='images\\save.png')
payment_icon = PhotoImage(file='images\\payments.png')
up = PhotoImage(file='images\\up.png')
down = PhotoImage(file='images\\down.png')
delete_btn = Image.open('images\\delete_icon.png')
delete_btn1 = ImageTk.PhotoImage(delete_btn)

pro_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')
sell_db = SellDatabase('login_signup_page\\manager_options\\manager_databases\\sell_db.db')
operations_db = Operations('login_signup_page\\manager_options\\manager_databases\\operations_db.db')

product_code = IntVar()
product_name = StringVar()
product_count = IntVar()
product_low_sell_price = StringVar()
product_buy_price = StringVar()
total_price = IntVar()
total_profit = IntVar()

#--------------------- Functions ---------------------
def display_products():
    products_table.delete(*products_table.get_children())
    for row in sell_db.fetch_products(bill_no):
        products_table.insert('', END, values=(row[0], row[2], row[4], row[5], row[6]), image=delete_btn1)

def get_json():
    global bill_no
    with open('data_file3.json', "r") as rf:
        if os.path.getsize('data_file3.json') != 0 and json.load(rf) != "":
            rf.seek(0)
            bill_no = json.load(rf)
            empty_data = ""
            with open('data_file3.json', "w") as wf:
                json.dump(empty_data, wf)
        else:
            bill_no = sell_db.fetch_last_bill_no()
get_json()

def add_product():
    sell_db.insert_product(
        total_profit_entry.get(),
        total_price_entry.get(),
        buy_price_entry.get(),
        low_sell_price_entry.get(),
        0,
        count_entry.get(),
        name_entry.get(),
        code_entry.get(),
        bill_no
    )
    pro_db.decrease_count(count_entry.get(), code_entry.get())
    clear()
    display_products()

def add_product_page():
    global code_entry, name_entry, count_entry, low_sell_price_entry, buy_price_entry, total_price_entry, total_profit_entry

    win = Tk()
    win_width = int(width*.4)
    win_height = int(height*.5)
    win.geometry(f'{win_width}x{win_height}+{int(width*.3)}+{int(win_height*.4)}')
    win.configure(bg='#ABB2B9')

    win_title = Label(win, text='إضافة منتج', bg='#117A65')
    win_title.pack(fill=X)

    code_lb = Label(win, text='كود المنتج', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    code_lb.place(x=win_width*.8, y=win_height*.08, width=win_width*.18, height=win_height*.07)
    code_entry = Entry(win, font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_code, justify=CENTER)
    code_entry.place(x=win_width*.3, y=win_height*.08, width=win_width*.5, height=win_height*.07)
    code_entry.focus()

    name_lb = Label(win, text='اسم المنتج', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    name_lb.place(x=win_width*.8, y=win_height*.2, width=win_width*.18, height=win_height*.07)
    name_entry = Entry(win, font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_name, justify=CENTER)
    name_entry.place(x=win_width*.3, y=win_height*.2, width=win_width*.5, height=win_height*.07)

    count_lb = Label(win, text='عدد القطع', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    count_lb.place(x=win_width*.8, y=win_height*.32, width=win_width*.18, height=win_height*.07)
    count_entry = Entry(win, font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_count, justify=CENTER)
    count_entry.place(x=win_width*.3, y=win_height*.32, width=win_width*.5, height=win_height*.07)
    
    low_sell_price_lb = Label(win, text='سعر البيع', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    low_sell_price_lb.place(x=win_width*.8, y=win_height*.44, width=win_width*.18, height=win_height*.07)
    low_sell_price_entry = Entry(win, font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_low_sell_price, justify=CENTER)
    low_sell_price_entry.place(x=win_width*.3, y=win_height*.44, width=win_width*.5, height=win_height*.07)
    
    buy_price_lb = Label(win, text=':سعر الشراء', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    buy_price_lb.place(x=win_width*.8, y=win_height*.56, width=win_width*.18, height=win_height*.07)
    buy_price_entry = Entry(win, bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, textvariable=product_buy_price, justify=CENTER)
    buy_price_entry.place(x=win_width*.3, y=win_height*.56, width=win_width*.5, height=win_height*.07)

    total_price_lb = Label(win, text=':السعر الإجمالى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    total_price_lb.place(x=win_width*.8, y=win_height*.68, width=win_width*.18, height=win_height*.07)
    total_price_entry = Entry(win, bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, textvariable=total_price, justify=CENTER)
    total_price_entry.place(x=win_width*.3, y=win_height*.68, width=win_width*.5, height=win_height*.07)

    total_profit_lb = Label(win, text=':الربح الإجمالى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    total_profit_lb.place(x=win_width*.8, y=win_height*.8, width=win_width*.18, height=win_height*.07)
    total_profit_entry = Entry(win, bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, textvariable=total_profit, justify=CENTER)
    total_profit_entry.place(x=win_width*.3, y=win_height*.8, width=win_width*.5, height=win_height*.07)

    add_product_btn = Button(win, text='إضافة منتج', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=add_product)
    add_product_btn.place(x=win_width*.6, y=win_height*.9, width=win_width*.2, height=win_height*.07)
    autocomplete_btn = Button(win, text='ملئ تلقائي', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=autocomplete)
    autocomplete_btn.place(x=win_width*.2, y=win_height*.9, width=win_width*.2, height=win_height*.07)

    win.mainloop()

def autocomplete():
    global product_code, product_name, product_low_sell_price, product_buy_price

    if code_entry.get() != "" and name_entry.get() != "" and pro_db.id_product_to_bill(code_entry.get()) != pro_db.name_product_to_bill(name_entry.get()):
        messagebox.showerror('خطأ', 'كود المنتج و الاسم غير متطابقان')
    elif code_entry.get() != "" and name_entry.get() != "":
        if count_entry.get() == "":
            messagebox.showerror('خطأ', 'يجب إدخال عدد القطع')
        if low_sell_price_entry.get() != "":
            data = pro_db.id_product_to_bill(code_entry.get())
            if data == []:
                messagebox.showerror('خطأ', 'لا يوجد منتجات متطابقة مع هذا الكود')
            else:
                rows = []
                for i in range(5):
                    rows.append(data[0][i])
                buy_price_entry.delete(0, END)
                buy_price_entry.insert(0, rows[4])
                total_price = str(int(low_sell_price_entry.get()) * int(count_entry.get()))
                total_price_entry.delete(0, END)
                total_price_entry.insert(0, total_price)
                total_profit = int(low_sell_price_entry.get()) * int(count_entry.get()) - int(rows[4]) * int(count_entry.get())
                total_profit_entry.delete(0, END)
                total_profit_entry.insert(0, total_profit)
        else:
            data = pro_db.id_product_to_bill(code_entry.get())
            if data == []:
                messagebox.showerror('خطأ', 'لا يوجد منتجات متطابقة مع هذا الكود')
            else:
                rows = []
                for i in range(5):
                    rows.append(data[0][i])
                low_sell_price_entry.delete(0, END)
                low_sell_price_entry.insert(END, rows[3])
                buy_price_entry.delete(0, END)
                buy_price_entry.insert(0, rows[4])
                total_price = str(int(low_sell_price_entry.get()) * int(count_entry.get()))
                total_price_entry.delete(0, END)
                total_price_entry.insert(0, total_price)
                total_profit = int(low_sell_price_entry.get()) * int(count_entry.get()) - int(rows[4]) * int(count_entry.get())
                total_profit_entry.delete(0, END)
                total_profit_entry.insert(0, total_profit)
    elif code_entry.get() != "" and name_entry.get() == "":
        if count_entry.get() == "":
            messagebox.showerror('خطأ', 'يجب إدخال عدد القطع')
        else:
            data = pro_db.id_product_to_bill(code_entry.get())
            if data == []:
                messagebox.showerror('خطأ', 'لا يوجد منتجات متطابقة مع هذا الكود')
            else:
                rows = []
                for i in range(5):
                    rows.append(data[0][i])
                name_entry.insert(END, rows[1])
                low_sell_price_entry.delete(0, END)
                low_sell_price_entry.insert(END, rows[3])
                buy_price_entry.delete(0, END)
                buy_price_entry.insert(0, rows[4])
                total_price = str(int(low_sell_price_entry.get()) * int(count_entry.get()))
                total_price_entry.delete(0, END)
                total_price_entry.insert(0, total_price)
                total_profit = int(low_sell_price_entry.get()) * int(count_entry.get()) - int(rows[4]) * int(count_entry.get())
                total_profit_entry.delete(0, END)
                total_profit_entry.insert(0, total_profit)
    elif name_entry.get() != "" and code_entry.get() == "":
        if count_entry.get() == "":
            messagebox.showerror('خطأ', 'يجب إدخال عدد القطع')
        else:
            data = pro_db.name_product_to_bill(name_entry.get())
            if data == []:
                messagebox.showerror('خطأ', 'لا يوجد منتجات متطابقة مع هذا الاسم')
            else:
                rows = []
                for i in range(5):
                    rows.append(data[0][i])
                code_entry.insert(END, rows[0])
                low_sell_price_entry.delete(0, END)
                low_sell_price_entry.insert(END, rows[3])
                buy_price_entry.delete(0, END)
                buy_price_entry.insert(0, rows[4])
                total_price = str(int(low_sell_price_entry.get()) * int(count_entry.get()))
                total_price_entry.delete(0, END)
                total_price_entry.insert(0, total_price)
                total_profit = int(low_sell_price_entry.get()) * int(count_entry.get()) - int(rows[4]) * int(count_entry.get())
                total_profit_entry.delete(0, END)
                total_profit_entry.insert(0, total_profit)

def update_totals():
    total_price = int(update_low_sell_price_entry.get()) * int(update_count_entry.get())
    update_total_price_entry.config(state=NORMAL)
    update_total_price_entry.delete(0, END)
    update_total_price_entry.insert(0, total_price)
    update_total_price_entry.config(state='readonly')
    total_profit = total_price - int(update_low_sell_price_entry.get()) * int(update_count_entry.get())
    update_total_profit_entry.config(state=NORMAL)
    update_total_profit_entry.delete(0, END)
    update_total_profit_entry.insert(0, total_profit)
    update_total_profit_entry.config(state='readonly')

def update_product():
    sell_db.update_product(
        str(int(update_total_price_entry.get()) - int(update_count_entry.get()) * int(update_buy_price_entry.get())),
        update_total_price_entry.get(),
        update_low_sell_price_entry.get(),
        0,
        update_count_entry.get(),
        update_code_entry.get()
    )
    display_products()

def hide_update_frame():
    update_frame.place_forget()

def update_product_page():
    global update_frame, update_code_entry, update_name_entry, update_count_entry, update_low_sell_price_entry, update_buy_price_entry, update_total_price_entry, update_total_profit_entry

    update_frame = Frame(root, bg='#ABB2B9')
    update_frame_width = int(width*.4)
    update_frame_height = int(height*.5)
    update_frame.place(x=width*.3, y=height*.2, width=update_frame_width, height=update_frame_height)

    title_frame = Frame(update_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='تعديل منتج', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_update_frame)
    close_btn.place(x=update_frame_width*.92, y=0, width=update_frame_width*.08, height=30)

    update_code_lb = Label(update_frame, text='كود المنتج', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_code_lb.place(x=update_frame_width*.8, y=update_frame_height*.08, width=update_frame_width*.18, height=update_frame_height*.07)
    update_code_entry = Entry(update_frame, font=('tajawal', 12, 'bold'), bd=0, fg='#117A65', state='readonly', readonlybackground='#ABB2B9', textvariable=product_code, justify=CENTER)
    update_code_entry.place(x=update_frame_width*.3, y=update_frame_height*.08, width=update_frame_width*.5, height=update_frame_height*.07)
    update_code_entry.config(state=NORMAL)
    update_code_entry.delete(0, END)
    update_code_entry.insert(0, item_data[4])
    update_code_entry.config(state='readonly')

    update_name_lb = Label(update_frame, text='اسم المنتج', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_name_lb.place(x=update_frame_width*.8, y=update_frame_height*.2, width=update_frame_width*.18, height=update_frame_height*.07)
    update_name_entry = Entry(update_frame, font=('tajawal', 12, 'bold'), bd=0, fg='#117A65', state='readonly', readonlybackground='#ABB2B9', textvariable=product_name, justify=CENTER)
    update_name_entry.place(x=update_frame_width*.3, y=update_frame_height*.2, width=update_frame_width*.5, height=update_frame_height*.07)
    update_name_entry.config(state=NORMAL)
    update_name_entry.delete(0, END)
    update_name_entry.insert(0, item_data[3])
    update_name_entry.config(state='readonly')

    update_count_lb = Label(update_frame, text='عدد القطع', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_count_lb.place(x=update_frame_width*.8, y=update_frame_height*.32, width=update_frame_width*.18, height=update_frame_height*.07)
    update_count_entry = Entry(update_frame, font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_count, justify=CENTER)
    update_count_entry.place(x=update_frame_width*.3, y=update_frame_height*.32, width=update_frame_width*.5, height=update_frame_height*.07)
    update_count_entry.delete(0, END)
    update_count_entry.insert(0, item_data[2])

    update_low_sell_price_lb = Label(update_frame, text='سعر البيع', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_low_sell_price_lb.place(x=update_frame_width*.8, y=update_frame_height*.44, width=update_frame_width*.18, height=update_frame_height*.07)
    update_low_sell_price_entry = Entry(update_frame, font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, textvariable=product_low_sell_price, justify=CENTER)
    update_low_sell_price_entry.place(x=update_frame_width*.3, y=update_frame_height*.44, width=update_frame_width*.5, height=update_frame_height*.07)
    update_low_sell_price_entry.delete(0, END)
    update_low_sell_price_entry.insert(0, item_data[1])

    update_buy_price_lb = Label(update_frame, text=':سعر الشراء', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_buy_price_lb.place(x=update_frame_width*.8, y=update_frame_height*.56, width=update_frame_width*.18, height=update_frame_height*.07)
    update_buy_price_entry = Entry(update_frame, fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, state='readonly', readonlybackground='#ABB2B9', textvariable=product_buy_price, justify=CENTER)
    update_buy_price_entry.place(x=update_frame_width*.3, y=update_frame_height*.56, width=update_frame_width*.5, height=update_frame_height*.07)
    info = pro_db.id_product_to_bill(item_data[4])
    low_sell_price = info[0][4]
    update_buy_price_entry.config(state=NORMAL)
    update_buy_price_entry.delete(0, END)
    update_buy_price_entry.insert(0, low_sell_price)
    update_buy_price_entry.config(state='readonly')

    update_total_price_lb = Label(update_frame, text=':السعر الإجمالى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_total_price_lb.place(x=update_frame_width*.8, y=update_frame_height*.68, width=update_frame_width*.18, height=update_frame_height*.07)
    update_total_price_entry = Entry(update_frame, fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, state='readonly', readonlybackground='#ABB2B9', textvariable=total_price, justify=CENTER)
    update_total_price_entry.place(x=update_frame_width*.3, y=update_frame_height*.68, width=update_frame_width*.5, height=update_frame_height*.07)
    update_total_price_entry.config(state=NORMAL)
    update_total_price_entry.delete(0, END)
    update_total_price_entry.insert(0, item_data[0])
    update_total_price_entry.config(state='readonly')

    global total_profit
    update_total_profit_lb = Label(update_frame, text=':الربح الإجمالى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_total_profit_lb.place(x=update_frame_width*.8, y=update_frame_height*.8, width=update_frame_width*.18, height=update_frame_height*.07)
    update_total_profit_entry = Entry(update_frame, fg='#117A65', font=('tajawal', 9, 'bold'), bd=0, state='readonly', readonlybackground='#ABB2B9', textvariable=total_profit, justify=CENTER)
    update_total_profit_entry.place(x=update_frame_width*.3, y=update_frame_height*.8, width=update_frame_width*.5, height=update_frame_height*.07)
    total_profit = int(item_data[0]) - int(update_buy_price_entry.get()) * int(item_data[2])
    update_total_profit_entry.config(state=NORMAL)
    update_total_profit_entry.delete(0, END)
    update_total_profit_entry.insert(0, total_profit)
    update_total_profit_entry.config(state='readonly')

    save_product_btn = Button(update_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=update_product)
    save_product_btn.place(x=update_frame_width*.6, y=update_frame_height*.9, width=update_frame_width*.2, height=update_frame_height*.07)
    update_product_btn = Button(update_frame, text='تعديل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=update_totals)
    update_product_btn.place(x=update_frame_width*.2, y=update_frame_height*.9, width=update_frame_width*.2, height=update_frame_height*.07)

def clear():
    code_entry.delete(0, END)
    name_entry.delete(0, END)
    count_entry.delete(0, END)
    buy_price_entry.delete(0, END)
    low_sell_price_entry.delete(0, END)
    total_price_entry.delete(0, END)
    total_profit_entry.delete(0, END)
    code_entry.focus()

def hide():
    save_frame.place_forget()

def update_total_change_page():
    global save_frame, discount_entry, payment_entry, total_entry, change_entry, profit_entry, total_prices, change
    save_frame = Frame(root, bg='#ABB2B9')
    save_frame_width = width*.4
    save_frame_height = height*.4
    save_frame.place(x=width*.3, y=height*.25, width=save_frame_width, height=save_frame_height)

    title_frame = Frame(save_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='خيارات الفواتير', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide)
    close_btn.place(x=save_frame_width*.92, y=0, width=save_frame_width*.08, height=30)

    discount_label = Label(save_frame, text='الخصم', bg='#ABB2B9', fg='#117A65', font=('tajawal', 10, 'bold'))
    discount_label.place(x=save_frame_width*.8, y=save_frame_height*.1, width=save_frame_width*.2, height=save_frame_height*.08)
    discount_entry = Entry(save_frame, bd=0, font=('tajawal', 12, 'bold'), highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    discount_entry.place(x=save_frame_width*.45, y=save_frame_height*.1, width=save_frame_width*.3, height=save_frame_height*.08)
    discount_entry.delete(0, END)
    discount_entry.insert(0, 0)
    discount_entry.focus()

    total_label = Label(save_frame, text='إجمالى الفاتورة', bg='#ABB2B9', fg='#117A65', font=('tajawal', 10, 'bold'))
    total_label.place(x=save_frame_width*.8, y=save_frame_height*.25, width=save_frame_width*.2, height=save_frame_height*.08)
    total_entry = Entry(save_frame, font=('tajawal', 12, 'bold'), state='readonly', readonlybackground='#ABB2B9', bd=0, justify=CENTER)
    total_entry.place(x=save_frame_width*.45, y=save_frame_height*.25, width=save_frame_width*.3, height=save_frame_height*.08)
    total_prices = 0
    for item in products_table.get_children():
        values = products_table.item(item, "values")
        total_prices += int(values[0])
    total_entry.config(state=NORMAL)
    total_entry.delete(0, END)
    total_entry.insert(0, total_prices)
    total_entry.config(state='readonly')

    payment_label = Label(save_frame, text='المبلغ المدفوع', font=('tajawal', 10, 'bold'), bg='#ABB2B9', fg='#117A65')
    payment_label.place(x=save_frame_width*.8, y=save_frame_height*.4, width=save_frame_width*.2, height=save_frame_height*.08)
    payment_entry = Entry(save_frame, font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    payment_entry.place(x=save_frame_width*.45, y=save_frame_height*.4, width=save_frame_width*.3, height=save_frame_height*.08)
    payment_entry.delete(0, END)
    payment_entry.insert(0, 0)
    
    change_label = Label(save_frame, text='الباقى', font=('tajawal', 10, 'bold'), bg='#ABB2B9', fg='#117A65')
    change_label.place(x=save_frame_width*.8, y=save_frame_height*.55, width=save_frame_width*.2, height=save_frame_height*.08)
    change_entry = Entry(save_frame, font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    change_entry.place(x=save_frame_width*.45, y=save_frame_height*.55, width=save_frame_width*.3, height=save_frame_height*.08)
    change = total_prices - int(payment_entry.get()) - int(discount_entry.get())
    change_entry.delete(0, END)
    change_entry.insert(0, change)

    profit_label = Label(save_frame, text='إجمالى الربح', font=('tajawal', 10, 'bold'), bg='#ABB2B9', fg='#117A65')
    profit_label.place(x=save_frame_width*.8, y=save_frame_height*.7, width=save_frame_width*.2, height=save_frame_height*.08)
    profit_entry = Entry(save_frame, font=('tajawal', 12, 'bold'), bd=0, state='readonly', readonlybackground='#ABB2B9', fg='#117A65', justify=CENTER)
    profit_entry.place(x=save_frame_width*.45, y=save_frame_height*.7, width=save_frame_width*.3, height=save_frame_height*.08)
    total_profit = 0
    for item in sell_db.fetch_product_total(bill_no):
        values = sell_db.fetch_product_total(bill_no)
        total_profit += int(values[0][0]) - int(values[0][1]) * int(values[0][3])
    real_profit = total_profit - int(discount_entry.get())
    print(real_profit)
    profit_entry.config(state=NORMAL)
    profit_entry.delete(0, END)
    profit_entry.insert(0, real_profit)
    profit_entry.config(state='readonly')

    update_btn = Button(save_frame, text='تعديل', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 12, 'bold'), cursor='hand2', command=update_total_change)
    update_btn.place(x=save_frame_width*.2, y=save_frame_height*.85, width=save_frame_width*.2, height=save_frame_height*.1)
    save_btn = Button(save_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 12, 'bold'), cursor='hand2', command= save)
    save_btn.place(x=save_frame_width*.6, y=save_frame_height*.85, width=save_frame_width*.2, height=save_frame_height*.1)

def save():
    sell_db.update_bill_total_change(change_entry.get(), total_entry.get(), bill_no)
    Popen(['python', 'login_signup_page\\manager_options\\sell.py'])
    quit()

def update_total_change():
    total_prices = 0
    for item in products_table.get_children():
        values = products_table.item(item, "values")
        total_prices += int(values[0])
    total_entry.config(state=NORMAL)
    total_entry.delete(0, END)
    total_entry.insert(0, total_prices)
    total_entry.config(state='readonly')

    change = total_prices - int(payment_entry.get()) - int(discount_entry.get())
    change_entry.delete(0, END)
    change_entry.insert(0, change)

    total_profit = 0
    for item in sell_db.fetch_products_info(bill_no):
        values = sell_db.fetch_products_info(bill_no)
        total_profit += int(values[0][0]) - int(values[0][1]) * int(values[0][4])
    real_profit = total_profit - int(discount_entry.get())
    profit_entry.config(state=NORMAL)
    profit_entry.delete(0, END)
    profit_entry.insert(0, real_profit)
    profit_entry.config(state='readonly')

def display_payments():
    payments_table.delete(*payments_table.get_children())
    for row in sell_db.fetch_payments(bill_no):
        payments_table.insert('', END, values=(row[0], row[2], row[1], row[4]), image=delete_btn1)

def add_payment():
    show_payments()
    operations_db.insert_operation('إضافة', 'عملية بيع فاتورة '+str(bill_no), quantity_entry.get())
    data = operations_db.fetch_last_operation()
    operation_no = data[0]
    sell_db.insert_payment(payer_entry.get(), quantity_entry.get(), operation_no, bill_no)
    clear_payment_page()
    payer_entry.focus()
    display_payments()

def clear_payment_page():
    payer_entry.delete(0, END)
    quantity_entry.delete(0, END)

def hide_payments_frame():
    payments_frame.place_forget()

def payment_page():
    global payments_frame, payer_entry, quantity_entry
    payments_frame = Frame(root, bg='#ABB2B9')
    payments_frame_width = width*.25
    payments_frame_height = height*.25
    payments_frame.place(x=width*.4, y=height*.35, width=payments_frame_width, height=payments_frame_height)

    title_frame = Frame(payments_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='خيارات الفواتير', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_payments_frame)
    close_btn.place(x=payments_frame_width*.92, y=0, width=payments_frame_width*.08, height=30)

    payer_lb = Label(payments_frame, text='المسدد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 11, 'bold'))
    payer_lb.place(x=payments_frame_width*.75, y=payments_frame_height*.2, width=payments_frame_width*.25, height=payments_frame_height*.1)
    payer_entry = Entry(payments_frame, fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    payer_entry.place(x=payments_frame_width*.25, y=payments_frame_height*.2, width=payments_frame_width*.5, height=payments_frame_height*.1)
    quantity_lb = Label(payments_frame, text='المبلغ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    quantity_lb.place(x=payments_frame_width*.75, y=payments_frame_height*.4, width=payments_frame_width*.25, height=payments_frame_height*.1)
    quantity_entry = Entry(payments_frame, fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    quantity_entry.place(x=payments_frame_width*.25, y=payments_frame_height*.4, width=payments_frame_width*.5, height=payments_frame_height*.1)
    date_lb = Label(payments_frame, text='تاريخ السداد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 11, 'bold'))
    date_lb.place(x=payments_frame_width*.75, y=payments_frame_height*.6, width=payments_frame_width*.25, height=payments_frame_height*.1)
    date_entry = Entry(payments_frame, fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    date_entry.place(x=payments_frame_width*.25, y=payments_frame_height*.6, width=payments_frame_width*.5, height=payments_frame_height*.1)
    date_entry.delete(0, END)
    date_entry.insert(0, date.today())
    add_payment_btn = Button(payments_frame, text='إضافة دفعة', bd=2, relief=SOLID, bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), cursor='hand2', command=add_payment)
    add_payment_btn.place(x=payments_frame_width*.3, y=payments_frame_height*.8, width=payments_frame_width*.4, height=payments_frame_height*.15)


def hide():
    save_frame.place_forget()

def save_page():
    global save_frame, discount_entry, total_prices, change, payments

    show_payments()
    total_prices = 0
    for item in products_table.get_children():
        values = products_table.item(item, "values")
        total_prices += int(values[0])

    payments = 0
    for item1 in payments_table.get_children():
        values1 = payments_table.item(item1, "values")
        payments += int(values1[2])
    change = total_prices - payments

    if change == 0:
        save()

    elif change != 0:
        save_frame = Frame(root, bg='#ABB2B9')
        save_frame_width = width*.25
        save_frame_height = height*.2
        save_frame.place(x=width*.4, y=height*.35, width=save_frame_width, height=save_frame_height)

        title_frame = Frame(save_frame, bg='#117A65')
        title_frame.pack(fill=X)
        title = Label(title_frame, text='حفظ الفاتورة', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
        title.pack()
        close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide)
        close_btn.place(x=save_frame_width*.92, y=0, width=save_frame_width*.08, height=30)

        discount_lb = Label(save_frame, text='الخصم', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
        discount_lb.place(x=save_frame_width*.75, y=save_frame_height*.25, width=save_frame_width*.25, height=save_frame_height*.15)
        discount_entry = Entry(save_frame, bd=0, font=('tajawal', 12, 'bold'), highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
        discount_entry.place(x=save_frame_width*.5, y=save_frame_height*.25, width=save_frame_width*.25, height=save_frame_height*.15)
        discount_entry.delete(0, END)
        discount_entry.insert(0, 0)
        discount_entry.focus()

        save_btn = Button(save_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 15, 'bold'), cursor='hand2', command=save)
        save_btn.place(x=save_frame_width*.3, y=save_frame_height*.7, width=save_frame_width*.4, height=save_frame_height*.2)


def save():
    sell_db.update_bill_total_change(total_prices, change, bill_no)
    Popen(['python', 'login_signup_page\\manager_options\\sell.py'])
    quit()

def on_treeview_click(event):
    global item_data
    selected_item = products_table.selection()
    item_data = products_table.item(selected_item, 'values')
    row_id = products_table.identify_row(event.y)
    column_id = products_table.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            sell_db.remove_product(item_data[4])
            pro_db.increase_count(item_data[2], item_data[4])
            display_products()
    if column_id == "#1" or column_id == "#2" or column_id == "#3" or column_id == "#4" or column_id == "#5":
        if row_id:
            update_product_page()

def on_payments_click(event):
    global payment_info
    selected_item1 = payments_table.selection()
    payment_info = payments_table.item(selected_item1, 'values')
    row_id = payments_table.identify_row(event.y)
    column_id = payments_table.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            operation_no = sell_db.fetch_operation_no(payment_info[3])
            operations_db.remove_operation(operation_no[0])
            sell_db.remove_payment(payment_info[3])
            display_payments()
    if column_id == "#1" or column_id == "#2" or column_id == "#3":
        if row_id:
            update_product_page()

def show_payments():
    display_payments()
    payments_table.place(x=0, y=30, width=view_frame_width, height=view_frame_height*.5)
    payments_title = Button(payments_title_frame, text='عمليات الدفع', image=up, compound=RIGHT, font=('tajawal', 9, 'bold'), bd=0, bg='#ABB2B9', cursor='hand2', command=hide_payments)
    payments_title.place(x=view_frame_width*.9, y=0, width=view_frame_width*.1, height=25)
    products_title_frame.place(x=0, y=view_frame_height*.5+30, width=view_frame_width, height=30)
    products_title = Button(products_title_frame, text='المنتجات', font=('tajawal', 10, 'bold'), bd=0, bg='#ABB2B9')
    products_title.place(x=view_frame_width*.9, y=0, width=view_frame_width*.1, height=25)
    products_table.place(x=0, y=view_frame_height*.5+60, width=view_frame_width, height=view_frame_height-(view_frame_height*.5+60))

def hide_payments():
    payments_table.place_forget()
    payments_title = Button(payments_title_frame, text='عمليات الدفع', image=down, compound=RIGHT, font=('tajawal', 9, 'bold'), bd=0, bg='#ABB2B9', cursor='hand2', command=show_payments)
    payments_title.place(x=view_frame_width*.9, y=0, width=view_frame_width*.1, height=25)
    products_title_frame.place(x=0, y=30, width=view_frame_width, height=30)
    products_table.place(x=0, y=61, width=view_frame_width, height=view_frame_height-61)

#------------------ UpSide Frame ------------------
upside_frame = Frame(root, bg='#117A65')
def go_back():
    Popen(['python', 'login_signup_page\\manager_options\\sell.py'])
    quit()

upside_frame_width = int(width)
upside_frame_height = int(height * .05)
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='المبيعات', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo = Label(upside_frame, image=sell_logo, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)

#--------------------- DownSide Frame -------------------------
downside_frame = Frame(root, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_product_page)
add_btn.place(x=downside_frame_width*.95, y=downside_frame_height*.1)
payment_btn = Button(downside_frame, image=payment_icon, bg='#117A65', bd=0, cursor='hand2', command=payment_page)
payment_btn.place(x=downside_frame_width*.9, y=downside_frame_height*.1)
save_btn = Button(downside_frame, image=save_icon, bg='#117A65', bd=0, cursor='hand2', command=save_page)
save_btn.place(x=downside_frame_width*.87, y=downside_frame_height*.1)

#------------------ View Bills Frame -------------------------------
view_frame = Frame(root, bg='#ABB2B9')
view_frame_width = width
view_frame_height = height - upside_frame_height - downside_frame_height - 60
view_frame.place(x=0, y=upside_frame_height, width=view_frame_width, height=view_frame_height)

payments_title_frame = Frame(view_frame, bg='#ABB2B9', bd=1, relief=SOLID)
payments_title_frame.place(x=0, y=0, width=view_frame_width, height=30)
payments_title= Button(payments_title_frame, text='عمليات الدفع', image=down, compound=RIGHT, font=('tajawal', 9, 'bold'), bd=0, bg='#ABB2B9', cursor='hand2', command=show_payments)
payments_title.place(x=view_frame_width*.9, y=1, width=view_frame_width*.1, height=25)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
payments_table = ttk.Treeview(view_frame,
                        columns=('date', 'payer', 'quantity', 'payment_no'))
Scroll_y1 = Scrollbar(payments_table, width=20, orient=VERTICAL)
Scroll_y1.pack(fill=Y, side=RIGHT)
Scroll_y1.config(cursor='hand2', command=payments_table.yview)
payments_table.config(yscrollcommand=Scroll_y1.set)

payments_table.heading('date', text='تاريخ الدفعة')
payments_table.heading('payer', text='المسدد')
payments_table.heading('quantity', text='المبلغ')
payments_table.heading('payment_no', text='رقم الدفعة')
payments_table.column('#0', width=int(view_frame_width*.1), anchor=CENTER)
payments_table.column('date', width=int(view_frame_width*.2), anchor=CENTER)
payments_table.column('payer', width=int(view_frame_width*.25), anchor=CENTER)
payments_table.column('quantity', width=int(view_frame_width*.25), anchor=CENTER)
payments_table.column('payment_no', width=int(view_frame_width*.2), anchor=CENTER)

products_title_frame = Frame(view_frame, bg='#ABB2B9', bd=1, relief=SOLID)
products_title_frame.place(x=0, y=31, width=view_frame_width, height=30)
products_title = Button(products_title_frame, text='المنتجات', font=('tajawal', 10, 'bold'), bd=0, bg='#ABB2B9')
products_title.place(x=view_frame_width*.9, y=1, width=view_frame_width*.1, height=25)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
products_table = ttk.Treeview(view_frame,
                        columns=('total_price', 'low_sell_price', 'count', 'products', 'product_no'))
Scroll_y = Scrollbar(products_table, width=20, orient=VERTICAL)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=products_table.yview)
products_table.config(yscrollcommand=Scroll_y.set)
products_table.place(x=0, y=61, width=view_frame_width, height=view_frame_height-61)

products_table.heading('total_price', text='السعر الإجمالى')
products_table.heading('low_sell_price', text='سعر البيع جملة')
products_table.heading('count', text='عدد القطع')
products_table.heading('products', text='المنتجات')
products_table.heading('product_no', text='كود المنتج')
products_table.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
products_table.column('total_price', width=int(view_frame_width*.15), anchor=CENTER)
products_table.column('low_sell_price', width=int(view_frame_width*.15), anchor=CENTER)
products_table.column('count', width=int(view_frame_width*.1), anchor=CENTER)
products_table.column('products', width=int(view_frame_width*.4), anchor=CENTER)
products_table.column('product_no', width=int(view_frame_width*.15), anchor=CENTER)

products_table.bind('<ButtonRelease-1>', on_treeview_click)
payments_table.bind('<ButtonRelease-1>', on_payments_click)

display_products()

root.mainloop()
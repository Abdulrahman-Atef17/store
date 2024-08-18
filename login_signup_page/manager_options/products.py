from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from manager_databases.products_db import ProductsDatabase
import json
from subprocess import Popen
#-------------------------- إنشاء نافذة البرنامج ----------------------------
root = Tk()
width = int(root.winfo_screenwidth())
height = int(root.winfo_screenheight())
root.state('zoomed')
root.title('Company Name')
root.config(bg='#ABB2B9')


#---------------------------- إنشاء المتغيرات ------------------------------------
search_icon = PhotoImage(file='images\\search_icon.png')
add_icon = PhotoImage(file='images\\add_icon.png')
back_icon = PhotoImage(file='images\\left_arrow.png')
search_icon = PhotoImage(file='images\\search.png')
x_icon = PhotoImage(file='images\\x_sign.png')

pro_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')

id = IntVar()
name = StringVar()
count = StringVar()
buy_price = StringVar()
low_sell_price = StringVar()
sell_price = StringVar()
trader = StringVar()
item = StringVar()
date_of_buy = StringVar()
search_by = StringVar()
search_var = StringVar()
#---------------------------- إنشاء الدوال ----------------------------------------
def get_data(event):
    selected_row = products_table.focus()
    data = products_table.item(selected_row)
    global row
    row = data['values']
    return row

def save(e):
    data = get_data(e)
    if data != "":
        with open('data_file.json', 'w') as wf:
            json.dump(data, wf)
        Popen(['python', 'login_signup_page\\manager_options\\update_product.py'])
    quit()


def delete():
    pro_db.remove(row[0])
    display_all()

def display_all():
    get_json()
    products_table.delete(*products_table.get_children())
    for row in pro_db.fetch():
        products_table.insert('', END, values=row)


def get_json():
    global got_item, got_trader, got_sell_price, got_low_sell_price, got_buy_price, got_count, got_name, got_id, got_date
    with open('data_file.json', 'r') as rf:
        if os.path.getsize('data_file.json') != 0 and os.path.getsize('data_file.json') > 2:
            data = json.load(rf)
            got_date, got_item, got_trader, got_sell_price, got_low_sell_price, got_buy_price, got_count, got_name, got_id= data
            got_id
            name.set(got_name)
            count.set(got_count)
            buy_price.set(got_buy_price)
            low_sell_price.set(got_low_sell_price)
            sell_price.set(got_sell_price)
            trader.set(got_trader)
            item.set(got_item)
            date_of_buy.set(got_date)
            pro_db.update(
                got_date, got_item, got_trader, got_sell_price, got_low_sell_price, got_buy_price, got_count, got_name, got_id
            )

def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()


#------------------Upside Frame ---------------------------
upside_frame = Frame(root, bg='#117A65')
upside_frame_height = 35
upside_frame_width = width
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='المنتجات', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo_img = PhotoImage(file='images\\logos\\products.png')
logo = Label(upside_frame, image=logo_img, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.005, y=upside_frame_height*.15)


#-------------- Downside Frame -------------------------------
def add_product_page():
    other_script_path = 'login_signup_page\\manager_options\\add_product.py'
    Popen(['python', other_script_path])
    quit()

def search_componenets():
    global search_combo, search_entry, search_btn, exit_search_btn
    search_combo = ttk.Combobox(downside_frame, justify='right', state='readonly', textvariable=search_by, font=('tajawal', 9, 'bold'))
    search_combo['values'] = ('الاسم', 'الصنف', 'الكود', 'المورد')
    search_combo.current(0)
    search_combo.place(x=downside_frame_width*.8, y=downside_frame_height*.1, width=downside_frame_width*.1)
    search_entry = Entry(downside_frame, fg='#117A65', textvariable=search_var, font=('tajawal', 9, 'bold'), justify=CENTER)
    search_entry.place(x=downside_frame_width*.64, y=downside_frame_height*.1, width=downside_frame_width*.15)

    search_btn = Button(downside_frame, text='بحث', bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), cursor='hand2', command=search)
    search_btn.place(x=downside_frame_width*.52, y=downside_frame_height*.05, width=downside_frame_width*.1)
    exit_search_btn = Button(downside_frame, image=x_icon, bg='#117A65', bd=0, cursor='hand2', command=exit_search)
    exit_search_btn.place(x=downside_frame_width*.48)

def exit_search():
    search_combo.place(width=0, height=0)
    search_entry.place(width=0, height=0)
    search_btn.place(width=0, height=0)
    exit_search_btn.place(width=0, height=0)
    display_all()

def search():
    if(search_combo.get() == ''):
        messagebox.showerror('خطأ', 'يجب اخيار عنصر البحث')
    elif (search_entry.get() == 0):
        messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
    elif(search_combo.get() == 'الاسم'):
        rows = pro_db.search_name(search_entry.get())
    elif(search_combo.get() == 'الصنف'):
        rows = pro_db.search_item(search_entry.get())
    elif(search_combo.get() == 'الكود'):
        rows = pro_db.search_id(search_entry.get())
    elif(search_combo.get() == 'المورد'):
        rows = pro_db.search_trader(search_entry.get())
    if len(rows) != 0:
        products_table.delete(*products_table.get_children())
        for row in rows:
            products_table.insert("", 'end', value=row)
    else:
        messagebox.showerror('خطأ', 'لا يوجد عنصر بهذا الاسم')

downside_frame = Frame(root, bg='#117A65')
downside_frame_height = height*.12
downside_frame_width = width
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_button = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_product_page)
add_button.place(x=downside_frame_width*.96, y=upside_frame_height*.1)
search_button = Button(downside_frame, image=search_icon, bg='#117A65', bd=0, cursor='hand2', command=search_componenets)
search_button.place(x=downside_frame_width*.92, y=upside_frame_height*.1)

#------------------ View Frame ------------------------------
show_frame = Frame(root, bg='#ABB2B9')
show_frame_width = width
show_frame_height = height-upside_frame_height-downside_frame_height
show_frame.place(x=0, y=upside_frame_height, width=show_frame_width, height=show_frame_height)

scroll_y = Scrollbar(show_frame, orient=VERTICAL, width=20)
table_style = ttk.Style()
table_style.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
products_table = ttk.Treeview(show_frame,
                            columns=('date_of_buy', 'item', 'trader', 'sell_price', 'low_sell_price', 'buy_price', 'count', 'name','id'),
                            yscrollcommand=scroll_y.set)
products_table.place(x=0, y=0, width= show_frame_width-20, height=show_frame_height)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(cursor='hand2', command=products_table.yview)

products_table['show'] = 'headings'
products_table.heading('date_of_buy', text='تاريخ الشراء')
products_table.heading('item', text='الصنف')
products_table.heading('trader', text='المورد')
products_table.heading('sell_price', text='سعر البيع قطاعي')
products_table.heading('low_sell_price', text='سعر البيع جملة')
products_table.heading('buy_price', text='سعر الشراء')
products_table.heading('count', text='عدد القطع')
products_table.heading('name', text='اسم المنتج')
products_table.heading('id', text='ID')

products_table.column('date_of_buy', width=int(width/9), anchor=CENTER)
products_table.column('item', width=int(width/9), anchor=CENTER)
products_table.column('trader', width=int(width/9), anchor=CENTER)
products_table.column('sell_price', width=int(width/9), anchor=CENTER)
products_table.column('low_sell_price', width=int(width/9), anchor=CENTER)
products_table.column('buy_price', width=int(width/9), anchor=CENTER)
products_table.column('count', width=int(width/9), anchor=CENTER)
products_table.column('name', width=int(width/9), anchor=CENTER)
products_table.column('id', width=int(width/9), anchor=CENTER)


display_all()
products_table.bind('<ButtonRelease-1>', save)

root.mainloop()
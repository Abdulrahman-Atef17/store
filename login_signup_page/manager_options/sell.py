from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen
import json
from PIL import Image, ImageTk
from manager_databases.sell_db import SellDatabase
from manager_databases.operations_db import Operations
from manager_databases.customers_db import CustomersDatabase

root = Tk()
root.state('zoomed')
root.title('Company Name')

#---------------- Variables ----------------------
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

sell_db = SellDatabase('login_signup_page\\manager_options\\manager_databases\\sell_db.db')
operations_db = Operations('login_signup_page\\manager_options\\manager_databases\\operations_db.db')
Customers_db = CustomersDatabase('login_signup_page\\manager_options\\manager_databases\\customers_db.db')

sell_logo = PhotoImage(file='images\\logos\\selling_bill.png')
back_icon = PhotoImage(file='images\\left_arrow.png')
add_icon = PhotoImage(file='images\\add_icon.png')
search_icon = PhotoImage(file='images\\search.png')
x_icon = PhotoImage(file='images\\x_sign.png')
delete_btn = Image.open('images\\delete_icon.png')  # Replace with your image file
delete_btn1 = ImageTk.PhotoImage(delete_btn)

search_by = StringVar()
search_var = StringVar()

#--------------------- Functions ---------------------
def display_all():
    sell_bills.delete(*sell_bills.get_children())
    for row in sell_db.fetch_bills():
        sell_bills.insert('', END, values=row, image=delete_btn1)

def update_bill():
    sell_db.update_bill(update_customer_name_entry.get(), item_data[4])
    display_all()
    win.place_forget()

def show_bill():
    if item_data != "":
        with open('data_file3.json', 'w') as wf:
            json.dump(item_data[4], wf)
    if (item_data[0] == 'قطاعى'):
        Popen(['python', 'login_signup_page\\manager_options\\sell_bill.py'])
    elif (item_data[0] == 'جملة'):
        Popen(['python', 'login_signup_page\\manager_options\\low_sell_bill.py'])
    root.destroy()

def update_bill_page():
    global win, update_bill_no_entry, update_customer_name_entry
    win = Frame(root, bg='#ABB2B9')
    win_width = int(width*.3)
    win_height = int(height*.3)
    win.place(x=width*.4, y=height*.35, width=win_width, height=win_height)
    
    title_frame = Frame(win, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='تعديل الفاتورة', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_options)
    close_btn.place(x=win_width*.92, y=0, width=win_width*.08, height=30)
    
    update_bill_no_lb = Label(win, text=':رقم الفاتورة', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65', justify=RIGHT)
    update_bill_no_lb.place(x=win_width*.75, y=win_height*.15, width=win_width*.2, height=win_height*.1)
    update_bill_no_entry = Entry(win, font=('tajawal', 12, 'bold'), fg='#117A65', bd=0, state='readonly', readonlybackground='#ABB2B9', justify=CENTER)
    update_bill_no_entry.place(x=win_width*.5, y=win_height*.15, width=win_width*.2, height=win_height*.1)
    update_bill_no_entry.config(state=NORMAL)
    update_bill_no_entry.delete(0, END)
    update_bill_no_entry.insert(0, item_data[4])
    update_bill_no_entry.config(state='readonly')

    update_customer_name_lb = Label(win, text='اسم العميل', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65')
    update_customer_name_lb.place(x=win_width*.75, y=win_height*.35, width=win_width*.2, height=win_height*.1)
    update_customer_name_entry = Entry(win, font=('tajawal', 9, 'bold'), justify=CENTER, bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2)
    update_customer_name_entry.place(x=win_width*.3, y=win_height*.36, width=win_width*.4, height=win_height*.08)
    update_customer_name_entry.focus()
    update_customer_name_entry.delete(0, END)
    update_customer_name_entry.insert(0, item_data[3])

    save_btn = Button(win, text='حفظ', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, cursor='hand2', command=update_bill)
    save_btn.place(x=win_width*.6, y=win_height*.7, width=win_width*.2, height=win_height*.1)
    show_bill_btn = Button(win, text='عرض الفاتورة', font=('tajawal', 10, 'bold'), bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, cursor='hand2', command=show_bill)
    show_bill_btn.place(x=win_width*.2, y=win_height*.7, width=win_width*.2, height=win_height*.1)

#------------------ UpSide Frame ---------------------
def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()

upside_frame = Frame(root, bg='#117A65')
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
def hide_add_options():
    win.place_forget()

def add_options():
    global win, bill_no_entry, customer_name_entry
    win = Frame(root, bg='#ABB2B9')
    win_width = int(width*.3)
    win_height = int(height*.3)
    win.place(x=width*.4, y=height*.3, width=win_width, height=win_height)
    
    title_frame = Frame(win, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='خيارات الفواتير', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_options)
    close_btn.place(x=win_width*.92, y=0, width=win_width*.08, height=30)
    
    if sell_db.fetch_last_bill_no():
        bill_no = int(sell_db.fetch_last_bill_no()) + 1
    else:
        bill_no = 1
    bill_no_lb = Label(win, text=':رقم الفاتورة', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65', justify=RIGHT)
    bill_no_lb.place(x=win_width*.75, y=win_height*.15, width=win_width*.2, height=win_height*.1)
    bill_no_entry = Entry(win, font=('tajawal', 12, 'bold'), fg='#117A65', bd=0, state='readonly', readonlybackground='#ABB2B9', justify=CENTER)
    bill_no_entry.place(x=win_width*.5, y=win_height*.15, width=win_width*.2, height=win_height*.1)
    bill_no_entry.config(state=NORMAL)
    bill_no_entry.delete(0, END)
    bill_no_entry.insert(0, bill_no)
    bill_no_entry.config(state='readonly')

    customer_name_lb = Label(win, text='اسم العميل', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65')
    customer_name_lb.place(x=win_width*.75, y=win_height*.35, width=win_width*.2, height=win_height*.1)
    customer_name_entry = Entry(win, font=('tajawal', 9, 'bold'), justify=CENTER, bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2)
    customer_name_entry.place(x=win_width*.3, y=win_height*.36, width=win_width*.4, height=win_height*.08)

    type_frame = Frame(win, bg='#ABB2B9')
    type_frame_width = win_width*.5
    type_frame_height = win_height*.4
    type_frame.place(x=win_width*.5, y=win_height*.5, width=type_frame_width, height=type_frame_height)
    type_title = Label(type_frame, text='اختر نوع الفاتورة', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65', justify=RIGHT)
    type_title.place(x=type_frame_width*.4, y=0, width=type_frame_width*.5, height=type_frame_height*.3)
    low_sell_btn = Button(type_frame, text='جملة', bd=0, font=('tajawal', 12, 'bold'), cursor='hand2', command=low_sell_page)
    low_sell_btn.place(x=type_frame_width*.1, y=type_frame_height*.4, width=type_frame_width*.8, height=type_frame_height*.2)
    separator = ttk.Separator(type_frame, orient=HORIZONTAL)
    separator.pack()
    sell_btn = Button(type_frame, text='قطاعى', bd=0, font=('tajawal', 12, 'bold'), cursor='hand2', command=sell_page)
    sell_btn.place(x=type_frame_width*.1, y=type_frame_height*.7, width=type_frame_width*.8, height=type_frame_height*.2)


def sell_page():
    if(customer_name_entry.get() == ""):
        messagebox.showerror('خطأ', 'يجب إدخال اسم العميل')
    else:
        sell_db.insert_bill('قطاعى', 0, 0, customer_name_entry.get())
        if not(Customers_db.check_existence(customer_name_entry.get())):
            Customers_db.insert_customer('قطاعى', '', '', customer_name_entry.get())
        Popen(['python', 'login_signup_page\\manager_options\\sell_bill.py'])
        quit()

def low_sell_page():
    if(customer_name_entry.get() == ""):
        messagebox.showerror('خطأ', 'يجب إدخال اسم العميل')
    else:
        sell_db.insert_bill('جملة', 0, 0, customer_name_entry.get())
        if not(Customers_db.check_existence(customer_name_entry.get())):
            Customers_db.insert_customer('جملة', '', '', customer_name_entry.get())
        Popen(['python', 'login_signup_page\\manager_options\\low_sell_bill.py'])
        quit()

def search_componenets():
    global search_combo, search_entry, search_btn, exit_search_btn
    search_combo = ttk.Combobox(downside_frame, justify='right', state='readonly', textvariable=search_by, font=('tajawal', 9, 'bold'))
    search_combo['values'] = ('اسم العميل', 'رقم الفاتورة', 'نوع الفاتورة')
    search_combo.current(0)
    search_combo.place(x=downside_frame_width*.8, y=downside_frame_height*.1, width=downside_frame_width*.1)
    search_entry = Entry(downside_frame, fg='#117A65', textvariable=search_var, font=('tajawal', 9, 'bold'), justify=CENTER)
    search_entry.place(x=downside_frame_width*.64, y=downside_frame_height*.1, width=downside_frame_width*.15)

    search_btn = Button(downside_frame, text='بحث', bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), cursor='hand2', command=search)
    search_btn.place(x=downside_frame_width*.52, y=downside_frame_height*.05, width=downside_frame_width*.1)
    exit_search_btn = Button(downside_frame, image=x_icon, bg='#117A65', bd=0)
    exit_search_btn.place(x=downside_frame_width*.48)

def exit_search():
    search_combo.place(width=0, height=0)
    search_entry.place(width=0, height=0)
    search_btn.place(width=0, height=0)
    exit_search_btn.place(width=0, height=0)

def search():
    if (search_entry.get() == 0):
        messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
    elif(search_combo.get() == 'نوع الفاتورة'):
        rows = sell_db.search_type(search_entry.get())
    elif(search_combo.get() == 'رقم الفاتورة'):
        rows = sell_db.search_bill_no(search_entry.get())
    elif(search_combo.get() == 'اسم العميل'):
        rows = sell_db.search_customer_name(search_entry.get())
    if len(rows) != 0:
        sell_bills.delete(*sell_bills.get_children())
        for row in rows:
            sell_bills.insert("", 'end', value=row)
    else:
        messagebox.showerror('خطأ', 'لا يوجد منتج مطابق للبيانات')

downside_frame = Frame(root, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_options)
add_btn.place(x=downside_frame_width*.95, y=downside_frame_height*.1)
search_btn = Button(downside_frame, image=search_icon, bg='#117A65', bd=0, cursor='hand2', command=search_componenets)
search_btn.place(x=downside_frame_width*.92, y=upside_frame_height*.1)

#------------------ View Bills Frame -------------------------------
def on_treeview_click(event):
    global item_data
    selected_item = sell_bills.selection()
    item_data = sell_bills.item(selected_item, 'values')
    row_id = sell_bills.identify_row(event.y)
    column_id = sell_bills.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            operation_no = sell_db.fetch_operation_no1(item_data[4])
            for i in range(len(operation_no)):
                operations_db.remove_operation(operation_no[i][0])
            sell_db.remove_bill(item_data[4])
            display_all()
    if column_id == "#1" or column_id == "#2" or column_id == "#3" or column_id == "#4" or column_id == "#5":
        if row_id:
            update_bill_page()

view_frame = Frame(root, bg='#ABB2B9')
view_frame_width = width
view_frame_height = height - upside_frame_height - downside_frame_height - 60
view_frame.place(x=0, y=upside_frame_height, width=view_frame_width, height=view_frame_height)

Scroll_y = Scrollbar(view_frame, width=20, orient=VERTICAL)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
sell_bills = ttk.Treeview(view_frame,
                        columns=('bill_type', 'change', 'total', 'customer_name', 'bill_no'),
                        yscrollcommand=Scroll_y.set)
sell_bills.place(x=0, y=0, width=view_frame_width-20, height=view_frame_height)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=sell_bills.yview)

sell_bills.heading('bill_type', text='نوع الفاتورة')
sell_bills.heading('change', text='الباقى')
sell_bills.heading('total', text='إجمالى الفاتورة')
sell_bills.heading('customer_name', text='اسم العميل')
sell_bills.heading('bill_no', text='رقم الفاتورة')
sell_bills.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
sell_bills.column('bill_type', width=int(view_frame_width*.2), anchor=CENTER)
sell_bills.column('change', width=int(view_frame_width*.1), anchor=CENTER)
sell_bills.column('total', width=int(view_frame_width*.15), anchor=CENTER)
sell_bills.column('customer_name', width=int(view_frame_width*.35), anchor=CENTER)
sell_bills.column('bill_no', width=int(view_frame_width*.15), anchor=CENTER)

sell_bills.bind("<ButtonRelease-1>", on_treeview_click)
display_all()

root.mainloop()
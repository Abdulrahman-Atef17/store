from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen
from PIL import Image, ImageTk
from manager_databases.traders_db import TradersDatabase
from manager_databases.buy_db import buyDatabase
from manager_databases.products_db import ProductsDatabase

root = Tk()
root.state('zoomed')
root.title('Company Name')

#---------------- Variables ----------------------
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

traders_db = TradersDatabase('login_signup_page\\manager_options\\manager_databases\\traders_db.db')
buy_db = buyDatabase('login_signup_page\\manager_options\\manager_databases\\buy_db.db')
products_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')

traders_logo = PhotoImage(file='images\\logos\\traders.png')
back_icon = PhotoImage(file='images\\left_arrow.png')
add_icon = PhotoImage(file='images\\add_icon.png')
search_icon = PhotoImage(file='images\\search.png')
x_icon = PhotoImage(file='images\\x_sign.png')
up = PhotoImage(file='images\\up.png')
down = PhotoImage(file='images\\down.png')
delete_btn = Image.open('images\\delete_icon.png')  # Replace with your image file
delete_btn1 = ImageTk.PhotoImage(delete_btn)

search_by = StringVar()
search_var = StringVar()

#-----------------------------------------------------------------------------
#----------------------------- Functions -------------------------------------
#-----------------------------------------------------------------------------
def go_back2():
    bill_frame.place_forget()
    bills_frame.place(x=0, y=0, width=width, height=height)

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

def display_payments():
    data = buy_db.fetch_bills_trader(item_data[3])
    for bill_no in data:
        payments_table.delete(*payments_table.get_children())
        for row in buy_db.fetch_payments(bill_no):
            payments_table.insert('', END, values=(row[0], row[1], row[3]))

def display_products():
    data = buy_db.fetch_bills_trader(item_data[2])
    bill_nos=[]
    for i in range(len(data)):
        bill_nos.append(data[i][4])
    for bill_no in bill_nos:
        products_table.delete(*products_table.get_children())
        for row in buy_db.fetch_products(bill_no):
            products_table.insert('', END, values=(row[0], row[1], row[2], row[3], row[4]))

def show_bill_page():
    global bill_frame, payments_table, products_table, payments_title_frame, products_title_frame
    bill_frame = Frame(root, bg='#ABB2B9')
    bill_frame_width = width
    bill_frame_height = height
    bill_frame.place(x=0, y=0, width=bill_frame_width, height=bill_frame_height)

    #------------------ UpSide Frame ------------------
    upside_frame = Frame(root, bg='#117A65')

    upside_frame_width = int(width)
    upside_frame_height = int(height * .05)
    upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

    title = Label(upside_frame, text='فاتورة '+item_data[2]+' رقم  '+item_data1[4], bg='#117A65', font=('tajawal', 15, 'bold'))
    title.pack()

    logo = Label(upside_frame, image=traders_logo, bg='#117A65')
    logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

    back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back2)
    back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)

    #------------------ View Bills Frame -------------------------------
    view_frame = Frame(root, bg='#ABB2B9')
    view_frame_width = width
    view_frame_height = height - upside_frame_height - 60
    view_frame.place(x=0, y=upside_frame_height, width=view_frame_width, height=view_frame_height)

    payments_title_frame = Frame(view_frame, bg='#ABB2B9', bd=1, relief=SOLID)
    payments_title_frame.place(x=0, y=0, width=view_frame_width, height=30)
    payments_title = Button(payments_title_frame, text='عمليات الدفع', image=down, compound=RIGHT, font=('tajawal', 9, 'bold'), bd=0, bg='#ABB2B9', cursor='hand2', command=show_payments)
    payments_title.place(x=view_frame_width*.9, y=1, width=view_frame_width*.1, height=25)
    list = ttk.Style()
    list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
    payments_table = ttk.Treeview(view_frame,
                            columns=('date', 'quantity', 'payment_no'))
    Scroll_y1 = Scrollbar(payments_table, width=20, orient=VERTICAL)
    Scroll_y1.pack(fill=Y, side=RIGHT)
    Scroll_y1.config(cursor='hand2', command=payments_table.yview)
    payments_table.config(yscrollcommand=Scroll_y1.set)

    payments_table['show'] = 'headings'
    payments_table.heading('date', text='تاريخ الدفعة')
    payments_table.heading('quantity', text='المبلغ')
    payments_table.heading('payment_no', text='رقم الدفعة')
    payments_table.column('date', width=int(view_frame_width*.4), anchor=CENTER)
    payments_table.column('quantity', width=int(view_frame_width*.4), anchor=CENTER)
    payments_table.column('payment_no', width=int(view_frame_width*.2), anchor=CENTER)

    products_title_frame = Frame(view_frame, bg='#ABB2B9', bd=1, relief=SOLID)
    products_title_frame.place(x=0, y=31, width=view_frame_width, height=30)
    products_title = Button(products_title_frame, text='المنتجات', font=('tajawal', 10, 'bold'), bd=0, bg='#ABB2B9')
    products_title.place(x=view_frame_width*.9, y=1, width=view_frame_width*.1, height=25)
    list = ttk.Style()
    list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
    products_table = ttk.Treeview(view_frame,
                            columns=('total_price', 'buy_price', 'count', 'products', 'product_no'))
    Scroll_y = Scrollbar(products_table, width=20, orient=VERTICAL)
    Scroll_y.pack(fill=Y, side=RIGHT)
    Scroll_y.config(cursor='hand2', command=products_table.yview)
    products_table.config(yscrollcommand=Scroll_y.set)
    products_table.place(x=0, y=61, width=view_frame_width, height=view_frame_height-61)

    products_table['show'] = 'headings'
    products_table.heading('total_price', text='السعر الإجمالى')
    products_table.heading('buy_price', text='سعر الشراء')
    products_table.heading('count', text='عدد القطع')
    products_table.heading('products', text='المنتجات')
    products_table.heading('product_no', text='كود المنتج')
    products_table.column('total_price', width=int(view_frame_width*.15), anchor=CENTER)
    products_table.column('buy_price', width=int(view_frame_width*.15), anchor=CENTER)
    products_table.column('count', width=int(view_frame_width*.1), anchor=CENTER)
    products_table.column('products', width=int(view_frame_width*.45), anchor=CENTER)
    products_table.column('product_no', width=int(view_frame_width*.15), anchor=CENTER)
    display_products()

def on_bills_click(event):
    global item_data1
    selected_item = bills.selection()
    item_data1 = bills.item(selected_item, 'values')
    row_id = bills.identify_row(event.y)
    column_id = bills.identify_column(event.x)
    if column_id == "#0" or column_id == "#1" or column_id == "#2" or column_id == "#3":
        if row_id:
            show_bill_page()

def go_back1():
    bills_frame.place_forget()
    main_frame.place(x=0, y=0, width=main_frame_width, height=main_frame_height)

i=0
def display_bills():
    global i
    bills.delete(*bills.get_children())
    for row in buy_db.fetch_bills_trader(item_data[2]):
        i += 1
        bills.insert('', END, values=(row[0], row[1], row[2], row[4], i))

rows1=[]
def search1():
            if(search_combo1.get() == ''):
                messagebox.showerror('خطأ', 'يجب اخيار عنصر البحث')
            elif (search_entry1.get() == 0):
                messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
            elif(search_combo1.get() == 'كود الفاتورة'):
                rows1 = buy_db.search_trader_bill_no(search_entry1.get(), item_data[2])
            elif(search_combo1.get() == 'تاريخ الفاتورة'):
                rows1 = buy_db.search_trader_date(search_entry1.get(), item_data[2])
            if len(rows1) != 0:
                bills.delete(*bills.get_children())
                iterator = 0
                for row in rows1:
                    iterator += 1
                    bills.insert("", 'end', value=(row[0], row[1], row[2], row[4], iterator))
            else:
                messagebox.showerror('خطأ', 'لا يوجد عنصر مطابق')

def exit_search1():
            search_combo1.place_forget()
            search_entry1.place_forget()
            search_btn1.place_forget()
            exit_search_btn1.place_forget()
            display_bills()

def search_componenets1():
        global search_combo1, search_entry1, search_btn1, exit_search_btn1
        search_combo1 = ttk.Combobox(downside_frame1, justify='right', state='readonly', textvariable=search_by, font=('tajawal', 9, 'bold'))
        search_combo1['values'] = ('تاريخ الفاتورة', 'كود الفاتورة')
        search_combo1.current(1)
        search_combo1.place(x=downside_frame_width1*.8, y=downside_frame_height*.1, width=downside_frame_width1*.1)
        search_entry1 = Entry(downside_frame1, fg='#117A65', textvariable=search_var, font=('tajawal', 9, 'bold'), justify=CENTER)
        search_entry1.place(x=downside_frame_width1*.64, y=downside_frame_height*.1, width=downside_frame_width1*.15)
        search_btn1 = Button(downside_frame1, text='بحث', bg='#ABB2B9', fg='#117A65', font=('tajawal', 9, 'bold'), cursor='hand2', command=search1)
        search_btn1.place(x=downside_frame_width1*.52, y=downside_frame_height*.05, width=downside_frame_width1*.1)
        exit_search_btn1 = Button(downside_frame1, image=x_icon, bg='#117A65', bd=0, cursor='hand2', command=exit_search1)
        exit_search_btn1.place(x=downside_frame_width1*.48)

def show_bills_page():
    main_frame.place_forget()
    update_frame.place_forget()
    global bills_frame, bills, downside_frame1, downside_frame_width1
    bills_frame = Frame(root, bg='#ABB2B9')
    bills_frame_width = width
    bills_frame_height = height
    bills_frame.place(x=0, y=0, width=bills_frame_width, height=bills_frame_height)

    upside_frame1 = Frame(bills_frame, bg='#117A65')
    upside_frame_width1 = int(bills_frame_width)
    upside_frame_height1 = int(bills_frame_height * .05)
    upside_frame1.place(x=0, y=0, width=upside_frame_width1, height=upside_frame_height1)

    title = Label(upside_frame1, text='فواتير '+(item_data[2]), bg='#117A65', font=('tajawal', 15, 'bold'))
    title.pack()

    logo = Label(upside_frame1, image=traders_logo, bg='#117A65')
    logo.place(x=upside_frame_width1*.95, y=upside_frame_height1*.1)

    back_btn = Button(upside_frame1, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back1)
    back_btn.place(x=upside_frame_width1*.02, y=upside_frame_height1*.1)

    #---------------------------------------- DownSide Frame ------------------------------
    downside_frame1 = Frame(bills_frame, bg='#117A65')
    downside_frame_width1 = int(width)
    downside_frame_height1 = int(height * .05)
    downside_frame1.place(x=0, y=height*.88, width=downside_frame_width1, height=downside_frame_height1)

    search_btn = Button(downside_frame1, image=search_icon, bg='#117A65', bd=0, cursor='hand2', command=search_componenets1)
    search_btn.place(x=downside_frame_width1*.95, y=upside_frame_height1*.1)

    #------------------------------------- View Frame -----------------------------------------
    view_frame1 = Frame(bills_frame, bg='#ABB2B9')
    view_frame_width1 = width
    view_frame_height1 = height - upside_frame_height1 - downside_frame_height1 - 60
    view_frame1.place(x=0, y=upside_frame_height1, width=view_frame_width1, height=view_frame_height1)

    Scroll_y = Scrollbar(view_frame1, width=20, orient=VERTICAL)
    list = ttk.Style()
    list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
    bills = ttk.Treeview(view_frame1,
                            columns=('date', 'change', 'total', 'bill_code',  'bill_no'),
                            yscrollcommand=Scroll_y.set)
    bills.place(x=0, y=0, width=view_frame_width1-20, height=view_frame_height1)
    Scroll_y.pack(fill=Y, side=RIGHT)
    Scroll_y.config(cursor='hand2', command=traders.yview)

    bills['show'] = 'headings'
    bills.heading('date', text='تاريخ الفاتورة')
    bills.heading('change', text='الباقى')
    bills.heading('total', text='إجمالى الفاتورة')
    bills.heading('bill_code', text='كود الفاتورة')
    bills.heading('bill_no', text='رقم الفاتورة')
    bills.column('date', anchor=CENTER)
    bills.column('change', anchor=CENTER)
    bills.column('total', anchor=CENTER)
    bills.column('bill_code', anchor=CENTER)
    bills.column('bill_no', anchor=CENTER)
    display_bills()
    bills.bind('<ButtonRelease-1>', on_bills_click)

def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()

def display_traders():
    traders.delete(*traders.get_children())
    for row in traders_db.fetch_traders():
        traders.insert('', END, values=(row[0], row[1], row[2], row[3]), image=delete_btn1)

def on_traders_click(event):
    global item_data
    selected_item = traders.selection()
    item_data = traders.item(selected_item, 'values')
    row_id = traders.identify_row(event.y)
    column_id = traders.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            traders_db.remove_trader(item_data[3])
            display_traders()
    if column_id == "#1" or column_id == "#2" or column_id == "#3":
        if row_id:
            update_page()

def hide_update_page():
    update_frame.place_forget()

def update():
    if(traders_db.check_existence(update_name_entry.get(), item_data[3])):
        messagebox.showerror('خطأ', 'هذا المورد موجود بالفعل')
    else:
        traders_db.update_trader(update_address_entry.get(), update_phone_entry.get(), update_name_entry.get(), update_id_entry.get())
        buy_db.update_bill_trader(update_name_entry.get(), item_data[2])
        products_db.update_product_trader(update_name_entry.get(), item_data[2])
        display_traders()

def update_page():
    global update_frame, update_id_entry, update_name_entry, update_phone_entry, update_address_entry
    update_frame = Frame(main_frame, bg='#ABB2B9')
    update_frame_width = int(width*.4)
    update_frame_height = int(height*.4)
    update_frame.place(x=width*.3, y=height*.25, width=update_frame_width, height=update_frame_height)

    title_frame = Frame(update_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='تعديل الفاتورة', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_update_page)
    close_btn.place(x=update_frame_width*.92, y=0, width=update_frame_width*.08, height=30)

    update_id_lb = Label(update_frame, text=':كود المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_id_lb.place(x=update_frame_width*.8, y=update_frame_height*.1, width=update_frame_width*.2, height=update_frame_height*.1)
    update_id_entry = Entry(update_frame, fg='#117A65', bd=0, state='readonly', readonlybackground='#ABB2B9', font=('tajawal', 12, 'bold'), justify=CENTER)
    update_id_entry.place(x=update_frame_width*.5, y=update_frame_height*.1, width=update_frame_width*.3, height=update_frame_height*.1)
    update_id_entry.config(state=NORMAL)
    update_id_entry.delete(0, END)
    update_id_entry.insert(0, item_data[3])
    update_id_entry.config(state='readonly')

    update_name_lb = Label(update_frame, text='اسم المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_name_lb.place(x=update_frame_width*.8, y=update_frame_height*.25, width=update_frame_width*.2, height=update_frame_height*.1)
    update_name_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_name_entry.place(x=update_frame_width*.4, y=update_frame_height*.25, width=update_frame_width*.4, height=update_frame_height*.1)
    update_name_entry.delete(0, END)
    update_name_entry.insert(0, item_data[2])

    update_phone_lb = Label(update_frame, text='رقم الهاتف', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_phone_lb.place(x=update_frame_width*.8, y=update_frame_height*.4, width=update_frame_width*.2, height=update_frame_height*.1)
    update_phone_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_phone_entry.place(x=update_frame_width*.4, y=update_frame_height*.4, width=update_frame_width*.4, height=update_frame_height*.1)
    update_phone_entry.delete(0, END)
    update_phone_entry.insert(0, item_data[1])

    update_address_lb = Label(update_frame, text='عنوان المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_address_lb.place(x=update_frame_width*.8, y=update_frame_height*.55, width=update_frame_width*.2, height=update_frame_height*.1)
    update_address_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_address_entry.place(x=update_frame_width*.4, y=update_frame_height*.55, width=update_frame_width*.4, height=update_frame_height*.1)
    update_address_entry.delete(0, END)
    update_address_entry.insert(0, item_data[0])

    save_btn = Button(update_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=update)
    save_btn.place(x=update_frame_width*.6, y=update_frame_height*.8, width=update_frame_width*.2, height=update_frame_height*.1)
    show_bills_btn = Button(update_frame, text='عرض الفواتير', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=show_bills_page)
    show_bills_btn.place(x=update_frame_width*.2, y=update_frame_height*.8, width=update_frame_width*.2, height=update_frame_height*.1)

def add_trader():
    if name_entry.get() == "":
        messagebox.showerror('خطأ', 'يجب ملئ حقل اسم المستخدم')
    elif (traders_db.check_existence1(name_entry.get())):
        messagebox.showerror('خطأ', 'هذا المورد موجود بالفعل')
    else:
        traders_db.insert_trader(address_entry.get(), phone_entry.get(), name_entry.get())
    display_traders()

def hide_add_page():
    add_frame.place_forget()

def add_trader_page():
    global add_frame, name_entry, phone_entry, address_entry
    add_frame = Frame(main_frame, bg='#ABB2B9')
    add_frame_width = int(width*.4)
    add_frame_height = int(height*.4)
    add_frame.place(x=width*.3, y=height*.25, width=add_frame_width, height=add_frame_height)

    title_frame = Frame(add_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='تعديل الفاتورة', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_page)
    close_btn.place(x=add_frame_width*.92, y=0, width=add_frame_width*.08, height=30)

    name_lb = Label(add_frame, text='اسم المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    name_lb.place(x=add_frame_width*.8, y=add_frame_height*.15, width=add_frame_width*.2, height=add_frame_height*.1)
    name_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    name_entry.place(x=add_frame_width*.4, y=add_frame_height*.15, width=add_frame_width*.4, height=add_frame_height*.1)

    phone_lb = Label(add_frame, text='رقم الهاتف', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    phone_lb.place(x=add_frame_width*.8, y=add_frame_height*.3, width=add_frame_width*.2, height=add_frame_height*.1)
    phone_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    phone_entry.place(x=add_frame_width*.4, y=add_frame_height*.3, width=add_frame_width*.4, height=add_frame_height*.1)

    address_lb = Label(add_frame, text='عنوان المورد', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    address_lb.place(x=add_frame_width*.8, y=add_frame_height*.45, width=add_frame_width*.2, height=add_frame_height*.1)
    address_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    address_entry.place(x=add_frame_width*.4, y=add_frame_height*.45, width=add_frame_width*.4, height=add_frame_height*.1)

    save_btn = Button(add_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=add_trader)
    save_btn.place(x=add_frame_width*.4, y=add_frame_height*.8, width=add_frame_width*.2, height=add_frame_height*.1)

def search_componenets():
    global search_combo, search_entry, search_btn, exit_search_btn
    search_combo = ttk.Combobox(downside_frame, justify='right', state='readonly', textvariable=search_by, font=('tajawal', 9, 'bold'))
    search_combo['values'] = ('عنوان المورد', 'كود المورد', 'اسم المورد')
    search_combo.current(2)
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
    display_traders()

def search():
    if(search_combo.get() == ''):
        messagebox.showerror('خطأ', 'يجب اخيار عنصر البحث')
    elif (search_entry.get() == 0):
        messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
    elif(search_combo.get() == 'اسم المورد'):
        rows = traders_db.search_name(search_entry.get())
    elif(search_combo.get() == 'كود المورد'):
        rows = traders_db.search_id(search_entry.get())
    elif(search_combo.get() == 'عنوان المورد'):
        rows = traders_db.search_address(search_entry.get())
    if len(rows) != 0:
        traders.delete(*traders.get_children())
        for row in rows:
            traders.insert("", 'end', value=row)
    else:
        messagebox.showerror('خطأ', 'لا يوجد عنصر بهذا الاسم')

#--------------------------------------------------------------------------------------
#-------------------------- UpSide Frame ----------------------------------------------
#--------------------------------------------------------------------------------------
main_frame = Frame(root, bg='#ABB2B9')
main_frame_width = width
main_frame_height = height
main_frame.place(x=0, y=0, width=main_frame_width, height=main_frame_height)
upside_frame = Frame(main_frame, bg='#117A65')
upside_frame_width = int(width)
upside_frame_height = int(height * .05)
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='الموردين', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo = Label(upside_frame, image=traders_logo, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)

#---------------------------------------- DownSide Frame ------------------------------
downside_frame = Frame(main_frame, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_trader_page)
add_btn.place(x=downside_frame_width*.95, y=downside_frame_height*.1)
search_btn = Button(downside_frame, image=search_icon, bg='#117A65', bd=0, cursor='hand2', command=search_componenets)
search_btn.place(x=downside_frame_width*.92, y=upside_frame_height*.1)

#------------------------------------- View Frame -----------------------------------------
view_frame = Frame(main_frame, bg='#ABB2B9')
view_frame_width = width
view_frame_height = height - upside_frame_height - downside_frame_height - 60
view_frame.place(x=0, y=upside_frame_height, width=view_frame_width, height=view_frame_height)

Scroll_y = Scrollbar(view_frame, width=20, orient=VERTICAL)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
traders = ttk.Treeview(view_frame,
                        columns=('address', 'phone_no', 'name', 'id'),
                        yscrollcommand=Scroll_y.set)
traders.place(x=0, y=0, width=view_frame_width-20, height=view_frame_height)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=traders.yview)

traders.heading('address', text='العنوان')
traders.heading('phone_no', text='رقم الهاتف')
traders.heading('name', text='اسم المورد')
traders.heading('id', text='كود المورد')
traders.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
traders.column('address', width=int(view_frame_width*.45), anchor=CENTER)
traders.column('phone_no', width=int(view_frame_width*.1), anchor=CENTER)
traders.column('name', width=int(view_frame_width*.3), anchor=CENTER)
traders.column('id', width=int(view_frame_width*.1), anchor=CENTER)

traders.bind('<ButtonRelease-1>', on_traders_click)
display_traders()

root.mainloop()
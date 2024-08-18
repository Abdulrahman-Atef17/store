from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen
from PIL import Image, ImageTk
from manager_databases.customers_db import CustomersDatabase
from manager_databases.sell_db import SellDatabase
from manager_databases.products_db import ProductsDatabase

root = Tk()
root.state('zoomed')
root.title('Company Name')

#---------------- Variables ----------------------
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

customers_db = CustomersDatabase('login_signup_page\\manager_options\\manager_databases\\customers_db.db')
sell_db = SellDatabase('login_signup_page\\manager_options\\manager_databases\\sell_db.db')
products_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')

customers_logo = PhotoImage(file='images\\logos\\customers.png')
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
    bill_nos = []
    data = sell_db.fetch_bills_customer(item_data[3])
    for i in range(len(data)):
        bill_nos.append(data[i][4])
    for bill_no in bill_nos:
        payments_table.delete(*payments_table.get_children())
        for row in sell_db.fetch_payments(bill_no):
            payments_table.insert('', END, values=(row[0], row[1], row[4]))

def display_products():
    data = sell_db.fetch_bills_customer(item_data[3])
    bill_nos=[]
    for i in range(len(data)):
        bill_nos.append(data[i][4])
    for bill_no in bill_nos:
        products_table.delete(*products_table.get_children())
        for row in sell_db.fetch_products(bill_no):
            products_table.insert('', END, values=(row[0], row[1], row[2], row[3], row[4]))

def show_bill_page():
    global payments_table, products_table, payments_title_frame, products_title_frame
    bill_frame = Frame(root, bg='#ABB2B9')
    bill_frame_width = width
    bill_frame_height = height
    bill_frame.place(x=0, y=0, width=bill_frame_width, height=bill_frame_height)

    #------------------ UpSide Frame ------------------
    upside_frame = Frame(root, bg='#117A65')

    upside_frame_width = int(width)
    upside_frame_height = int(height * .05)
    upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

    title = Label(upside_frame, text='فاتورة ', bg='#117A65', font=('tajawal', 15, 'bold'))
    title.pack()

    logo = Label(upside_frame, image=customers_logo, bg='#117A65')
    logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

    back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
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
    row_id = bills.identify_row(event.y)
    column_id = bills.identify_column(event.x)
    if column_id == "#0" or column_id == "#1" or column_id == "#2" or column_id == "#3" or column_id == "#4":
        if row_id:
            show_bill_page()

def go_back1():
    bills_frame.place_forget()

i=0
def display_bills():
    global i
    bills.delete(*bills.get_children())
    for row in sell_db.fetch_bills_customer(item_data[3]):
        i += 1
        bills.insert('', END, values=(row[0], row[1], row[2], row[4], i))

rows1=[]
def search1():
            if(search_combo1.get() == ''):
                messagebox.showerror('خطأ', 'يجب اخيار عنصر البحث')
            elif (search_entry1.get() == 0):
                messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
            elif(search_combo1.get() == 'كود الفاتورة'):
                rows1 = sell_db.search_customer_bill_no(search_entry1.get(), item_data[3])
            elif(search_combo1.get() == 'تاريخ الفاتورة'):
                rows1 = sell_db.search_customer_date(search_entry1.get(), item_data[3])
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

    logo = Label(upside_frame1, image=customers_logo, bg='#117A65')
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
    Scroll_y.config(cursor='hand2', command=customers.yview)

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

def display_customers():
    customers.delete(*customers.get_children())
    for row in customers_db.fetch_customers():
        customers.insert('', END, values=(row[0], row[1], row[2], row[3], row[4]), image=delete_btn1)

def on_customers_click(event):
    global item_data
    selected_item = customers.selection()
    item_data = customers.item(selected_item, 'values')
    row_id = customers.identify_row(event.y)
    column_id = customers.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            customers_db.remove_customer(item_data[4])
            display_customers()
    if column_id == "#1" or column_id == "#2" or column_id == "#3" or column_id == "#4":
        if row_id:
            update_page()

def hide_update_page():
    update_frame.place_forget()

def update():
    if(customers_db.check_existence(update_name_entry.get(), item_data[3])):
        messagebox.showerror('خطأ', 'هذا العميل موجود بالفعل')
    else:
        customers_db.update_customer(update_type_combo.get(), update_address_entry.get(), update_phone_entry.get(), update_name_entry.get(), update_id_entry.get())
        sell_db.update_bill_customer(update_name_entry.get(), item_data[3])
        display_customers()

def update_page():
    global update_frame, update_id_entry, update_name_entry, update_phone_entry, update_address_entry, update_type_combo
    update_frame = Frame(main_frame, bg='#ABB2B9')
    update_frame_width = int(width*.4)
    update_frame_height = int(height*.4)
    update_frame.place(x=width*.3, y=height*.25, width=update_frame_width, height=update_frame_height)

    title_frame = Frame(update_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='تعديل بيانات العميل', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_update_page)
    close_btn.place(x=update_frame_width*.92, y=0, width=update_frame_width*.08, height=30)

    update_id_lb = Label(update_frame, text=':كود العميل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_id_lb.place(x=update_frame_width*.8, y=update_frame_height*.1, width=update_frame_width*.2, height=update_frame_height*.1)
    update_id_entry = Entry(update_frame, fg='#117A65', bd=0, state='readonly', readonlybackground='#ABB2B9', font=('tajawal', 12, 'bold'), justify=CENTER)
    update_id_entry.place(x=update_frame_width*.5, y=update_frame_height*.1, width=update_frame_width*.3, height=update_frame_height*.1)
    update_id_entry.config(state=NORMAL)
    update_id_entry.delete(0, END)
    update_id_entry.insert(0, item_data[4])
    update_id_entry.config(state='readonly')

    update_name_lb = Label(update_frame, text='اسم العميل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_name_lb.place(x=update_frame_width*.8, y=update_frame_height*.25, width=update_frame_width*.2, height=update_frame_height*.1)
    update_name_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_name_entry.place(x=update_frame_width*.4, y=update_frame_height*.25, width=update_frame_width*.4, height=update_frame_height*.1)
    update_name_entry.delete(0, END)
    update_name_entry.insert(0, item_data[3])

    update_phone_lb = Label(update_frame, text='رقم الهاتف', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_phone_lb.place(x=update_frame_width*.8, y=update_frame_height*.4, width=update_frame_width*.2, height=update_frame_height*.1)
    update_phone_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_phone_entry.place(x=update_frame_width*.4, y=update_frame_height*.4, width=update_frame_width*.4, height=update_frame_height*.1)
    update_phone_entry.delete(0, END)
    update_phone_entry.insert(0, item_data[2])

    update_address_lb = Label(update_frame, text='عنوان العميل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_address_lb.place(x=update_frame_width*.8, y=update_frame_height*.55, width=update_frame_width*.2, height=update_frame_height*.1)
    update_address_entry = Entry(update_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    update_address_entry.place(x=update_frame_width*.4, y=update_frame_height*.55, width=update_frame_width*.4, height=update_frame_height*.1)
    update_address_entry.delete(0, END)
    update_address_entry.insert(0, item_data[1])
    
    update_type_lb = Label(update_frame, text='جملة/قطاعى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    update_type_lb.place(x=update_frame_width*.8, y=update_frame_height*.7, width=update_frame_width*.2, height=update_frame_height*.1)
    update_type_combo = ttk.Combobox(update_frame, font=('tajawal', 12, 'bold'), justify=CENTER, state='readonly')
    update_type_combo.place(x=update_frame_width*.5, y=update_frame_height*.7, width=update_frame_width*.3, height=update_frame_height*.1)
    update_type_combo['values'] = ('جملة', 'قطاعى')
    update_type_combo.config(state=NORMAL)
    update_type_combo.delete(0, END)
    update_type_combo.insert(0, item_data[0])
    update_type_combo.config(state='readonly')

    save_btn = Button(update_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=update)
    save_btn.place(x=update_frame_width*.6, y=update_frame_height*.85, width=update_frame_width*.2, height=update_frame_height*.1)
    show_bills_btn = Button(update_frame, text='عرض الفواتير', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=show_bills_page)
    show_bills_btn.place(x=update_frame_width*.2, y=update_frame_height*.85, width=update_frame_width*.2, height=update_frame_height*.1)

def add_customer():
    if name_entry.get() == "":
        messagebox.showerror('خطأ', 'يجب ملئ حقل اسم العميل')
    elif (customers_db.check_existence(name_entry.get())):
        messagebox.showerror('خطأ', 'هذا العميل موجود بالفعل')
    else:
        customers_db.insert_customer(type_combo.get(), address_entry.get(), phone_entry.get(), name_entry.get())
    display_customers()

def hide_add_page():
    add_frame.place_forget()

def add_customer_page():
    global add_frame, name_entry, phone_entry, address_entry, type_combo
    add_frame = Frame(main_frame, bg='#ABB2B9')
    add_frame_width = int(width*.4)
    add_frame_height = int(height*.4)
    add_frame.place(x=width*.3, y=height*.25, width=add_frame_width, height=add_frame_height)

    title_frame = Frame(add_frame, bg='#117A65')
    title_frame.pack(fill=X)
    title = Label(title_frame, text='إضافة عميل', bg='#117A65', fg='white', font=('tajawal', 12, 'bold'))
    title.pack()
    close_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_page)
    close_btn.place(x=add_frame_width*.92, y=0, width=add_frame_width*.08, height=30)

    name_lb = Label(add_frame, text='اسم العميل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    name_lb.place(x=add_frame_width*.8, y=add_frame_height*.15, width=add_frame_width*.2, height=add_frame_height*.1)
    name_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    name_entry.place(x=add_frame_width*.4, y=add_frame_height*.15, width=add_frame_width*.4, height=add_frame_height*.1)

    phone_lb = Label(add_frame, text='رقم الهاتف', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    phone_lb.place(x=add_frame_width*.8, y=add_frame_height*.3, width=add_frame_width*.2, height=add_frame_height*.1)
    phone_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    phone_entry.place(x=add_frame_width*.4, y=add_frame_height*.3, width=add_frame_width*.4, height=add_frame_height*.1)

    address_lb = Label(add_frame, text='عنوان العميل', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    address_lb.place(x=add_frame_width*.8, y=add_frame_height*.45, width=add_frame_width*.2, height=add_frame_height*.1)
    address_entry = Entry(add_frame, fg='#117A65', bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, font=('tajawal', 12, 'bold'), justify=CENTER)
    address_entry.place(x=add_frame_width*.4, y=add_frame_height*.45, width=add_frame_width*.4, height=add_frame_height*.1)

    type_lb = Label(add_frame, text='جملة/قطاعى', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    type_lb.place(x=add_frame_width*.8, y=add_frame_height*.6, width=add_frame_width*.2, height=add_frame_height*.1)
    type_combo = ttk.Combobox(add_frame, font=('tajawal', 12, 'bold'), justify=CENTER, state='readonly')
    type_combo.place(x=add_frame_width*.5, y=add_frame_height*.6, width=add_frame_width*.3, height=add_frame_height*.1)
    type_combo['values'] = ('جملة', 'قطاعى')
    type_combo.current(0)

    save_btn = Button(add_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'), bd=2, relief=SOLID, cursor='hand2', command=add_customer)
    save_btn.place(x=add_frame_width*.4, y=add_frame_height*.85, width=add_frame_width*.2, height=add_frame_height*.1)

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
    display_customers()

def search():
    if(search_combo.get() == ''):
        messagebox.showerror('خطأ', 'يجب اخيار عنصر البحث')
    elif (search_entry.get() == 0):
        messagebox.showerror('خطأ', 'اكتب عنصرا للبحث عنه')
    elif(search_combo.get() == 'اسم العميل'):
        rows = customers_db.search_name(search_entry.get())
    elif(search_combo.get() == 'كود العميل'):
        rows = customers_db.search_id(search_entry.get())
    elif(search_combo.get() == 'عنوان العميل'):
        rows = customers_db.search_address(search_entry.get())
    elif(search_combo.get() == 'جملة/قطاعى'):
        rows = customers_db.search_type(search_entry.get())
    if len(rows) != 0:
        customers.delete(*customers.get_children())
        for row in rows:
            customers.insert("", 'end', value=row)
    else:
        messagebox.showerror('خطأ', 'لا يوجد عنصر مطابق')

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

title = Label(upside_frame, text='العملاء', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo = Label(upside_frame, image=customers_logo, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)

#---------------------------------------- DownSide Frame ------------------------------
downside_frame = Frame(main_frame, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_customer_page)
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
customers = ttk.Treeview(view_frame,
                        columns=('type', 'address', 'phone_no', 'name', 'id'),
                        yscrollcommand=Scroll_y.set)
customers.place(x=0, y=0, width=view_frame_width-20, height=view_frame_height)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=customers.yview)

customers.heading('type', text='جملة/قطاعى')
customers.heading('address', text='العنوان')
customers.heading('phone_no', text='رقم الهاتف')
customers.heading('name', text='اسم العميل')
customers.heading('id', text='كود العميل')
customers.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
customers.column('type', width=int(view_frame_width*.1), anchor=CENTER)
customers.column('address', width=int(view_frame_width*.3), anchor=CENTER)
customers.column('phone_no', width=int(view_frame_width*.15), anchor=CENTER)
customers.column('name', width=int(view_frame_width*.3), anchor=CENTER)
customers.column('id', width=int(view_frame_width*.1), anchor=CENTER)

customers.bind('<ButtonRelease-1>', on_customers_click)
display_customers()

root.mainloop()
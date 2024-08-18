from tkinter import *
from tkinter import ttk
from subprocess import Popen

from PIL import Image, ImageTk
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
delete_btn = Image.open('images\\delete_icon.png')
delete_btn1 = ImageTk.PhotoImage(delete_btn)

operations_db = Operations('login_signup_page\\manager_options\\manager_databases\\operations_db.db')

#--------------------- Functions ---------------------
def display_all():
    opertaions_table.delete(*opertaions_table.get_children())
    for row in operations_db.fetch_operations():
        opertaions_table.insert('', END, values=row, image=delete_btn1)

def hide_add_operation_page():
    add_operation_frame.place_forget()

def add_money():
    global money
    money = 0
    operations_db.insert_operation('إضافة', source_entry.get(), quantity_entry.get())
    data = operations_db.fetch_operations()
    for i in range(len(data)):
        if data[i][1] == 'إضافة':
            money += int(data[i][3])
        else:
            money -= int(data[i][3])
    money_screen.config(state='normal')
    money_screen.delete(0, END)
    money_screen.insert(0, money)
    money_screen.config(state='readonly')
    display_all()
    add_operation_frame.place_forget()

def take_money():
    global money
    money = 0
    operations_db.insert_operation('سحب', source_entry.get(), quantity_entry.get())
    data = operations_db.fetch_operations()
    for i in range(len(data)):
        if data[i][1] == 'إضافة':
            money += int(data[i][3])
        else:
            money -= int(data[i][3])
    money_screen.config(state='normal')
    money_screen.delete(0, END)
    money_screen.insert(0, money)
    money_screen.config(state='readonly')
    display_all()
    add_operation_frame.place_forget()

def add_operation_page():
    global add_operation_frame, quantity_entry, source_entry
    add_operation_frame = Frame(root, bg='#ABB2B9')
    add_operation_frame_width = width * .35
    add_operation_frame_height = height * .25
    add_operation_frame.place(x=width*.35, y=height*.3, width=add_operation_frame_width, height=add_operation_frame_height)

    title_frame = Frame(add_operation_frame, bg='#117A65')
    title_frame.place(x=0, y=0, width=add_operation_frame_width, height=30)
    title = Label(title_frame, text='إضافة عملية', bg='#117A65', font=('tajawal', 12, 'bold'))
    title.pack()
    exit_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_operation_page)
    exit_btn.place(x=add_operation_frame_width*.92, y=0, width=add_operation_frame_width*.08, height=30)

    quantity_lb = Label(add_operation_frame, text='المبلغ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    quantity_lb.place(x=add_operation_frame_width*.7, y=add_operation_frame_height*.2, width=add_operation_frame_width*.3, height=add_operation_frame_height*.1)
    quantity_entry = Entry(add_operation_frame,  fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    quantity_entry.place(x=add_operation_frame_width*.3, y=add_operation_frame_height*.2, width=add_operation_frame_width*.4, height=add_operation_frame_height*.1)
    source_lb = Label(add_operation_frame, text='مصدر المال/الإنفاق', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    source_lb.place(x=add_operation_frame_width*.7, y=add_operation_frame_height*.4, width=add_operation_frame_width*.3, height=add_operation_frame_height*.1)
    source_entry = Entry(add_operation_frame,  fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    source_entry.place(x=add_operation_frame_width*.3, y=add_operation_frame_height*.4, width=add_operation_frame_width*.4, height=add_operation_frame_height*.1)
    add_btn = Button(add_operation_frame, text='إضافة المبلغ', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 12, 'bold'), cursor='hand2', command=add_money)
    add_btn.place(x=add_operation_frame_width*.6, y=add_operation_frame_height*.75, width=add_operation_frame_width*.2, height=add_operation_frame_height*.15)
    add_btn = Button(add_operation_frame, text='سحب المبلغ', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 12, 'bold'), cursor='hand2', command=take_money)
    add_btn.place(x=add_operation_frame_width*.2, y=add_operation_frame_height*.75, width=add_operation_frame_width*.2, height=add_operation_frame_height*.15)
#------------------ UpSide Frame ------------------
upside_frame = Frame(root, bg='#117A65')
def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()

upside_frame_width = int(width)
upside_frame_height = int(height * .05)
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='الصندوق', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo = Label(upside_frame, image=sell_logo, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)

#------------------------------ Money Quantity Frame ---------------------------
money_frame = Frame(root, bg='#117A65')
money_frame_width = width
money_frame_height = height*.05
money_frame.place(x=0, y=upside_frame_height+5, width=money_frame_width, height=money_frame_height)

money_screen = Entry(money_frame, font=('tajawal', 12, 'bold'), bd=0, state='readonly', justify=CENTER)
money_screen.place(x=money_frame_width*.4, y=10, width=money_frame_width*.2, height=money_frame_height-20)
money = 0
data = operations_db.fetch_operations()
for i in range(len(data)):
    if data[i][1] == 'إضافة':
        money += int(data[i][3])
    else:
        money -= int(data[i][3])
money_screen.config(state=NORMAL)
money_screen.delete(0, END)
money_screen.insert(0, money)
money_screen.config(state='readonly')

#--------------------- DownSide Frame -------------------------
downside_frame = Frame(root, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_operation_page)
add_btn.place(x=downside_frame_width*.95, y=downside_frame_height*.1)

#------------------ View Bills Frame -------------------------------
def on_treeview_click(event):
    global item_data
    money = 0
    selected_item = opertaions_table.selection()
    item_data = opertaions_table.item(selected_item, 'values')
    row_id = opertaions_table.identify_row(event.y)
    column_id = opertaions_table.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            operations_db.remove_operation(item_data[4])
            data = operations_db.fetch_operations()
        for i in range(len(data)):
            if data[i][1] == 'إضافة':
                money += int(data[i][3])
            else:
                money -= int(data[i][3])
        money_screen.config(state='normal')
        money_screen.delete(0, END)
        money_screen.insert(0, money)
        money_screen.config(state='readonly')
        display_all()

view_frame = Frame(root, bg='#ABB2B9')
view_frame_width = width
view_frame_height = height - upside_frame_height - downside_frame_height - money_frame_height - 60
view_frame.place(x=0, y=upside_frame_height+money_frame_height, width=view_frame_width, height=view_frame_height)

Scroll_y = Scrollbar(view_frame, width=20, orient=VERTICAL)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
opertaions_table = ttk.Treeview(view_frame,
                        columns=('date', 'type', 'source', 'quantity', 'operation_no'),
                        yscrollcommand=Scroll_y.set)
opertaions_table.place(x=0, y=0, width=view_frame_width-20, height=view_frame_height)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=opertaions_table.yview)

opertaions_table.heading('date', text='تاريخ العملية')
opertaions_table.heading('type', text='نوع العملية')
opertaions_table.heading('source', text='مصدر المال/الإنفاق')
opertaions_table.heading('quantity', text='المبلغ')
opertaions_table.heading('operation_no', text='رقم العملية')
opertaions_table.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
opertaions_table.column('date', width=int(view_frame_width*.15), anchor=CENTER)
opertaions_table.column('type', width=int(view_frame_width*.1), anchor=CENTER)
opertaions_table.column('source', width=int(view_frame_width*.35), anchor=CENTER)
opertaions_table.column('quantity', width=int(view_frame_width*.2), anchor=CENTER)
opertaions_table.column('operation_no', width=int(view_frame_width*.05), anchor=CENTER)

opertaions_table.bind('<ButtonRelease-1>', on_treeview_click)

display_all()

root.mainloop()
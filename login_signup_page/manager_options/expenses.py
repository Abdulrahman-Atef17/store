from tkinter import *
from tkinter import ttk
from subprocess import Popen

from PIL import Image, ImageTk
from manager_databases.expenses_db import ExpensesDatabase
from manager_databases.operations_db import Operations

root = Tk()
root.state('zoomed')
root.title('Company Name')

#---------------- Variables ----------------------
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

expenses_logo = PhotoImage(file='images\\logos\\expenses.png')
back_icon = PhotoImage(file='images\\left_arrow.png')
add_icon = PhotoImage(file='images\\add_icon.png')
delete_btn = Image.open('images\\delete_icon.png')
delete_btn1 = ImageTk.PhotoImage(delete_btn)

expenses_db = ExpensesDatabase('login_signup_page\\manager_options\\manager_databases\\expenses_db.db')
operations_db = Operations('login_signup_page\\manager_options\\manager_databases\\operations_db.db')

#--------------------- Functions ---------------------
def display_all():
    expenses_table.delete(*expenses_table.get_children())
    for row in expenses_db.fetch_expenses():
        expenses_table.insert('', END, values=(row[0], row[1], row[2], row[4]), image=delete_btn1)

def add_expenses():
    operations_db.insert_operation('سحب', source_entry.get(), quantity_entry.get())
    data = operations_db.fetch_last_operation()
    operation_no = data[0]
    expenses_db.insert_expenses(source_entry.get(), quantity_entry.get(), operation_no)
    display_all()

def hide_add_expenses_page():
    add_expenses_frame.place_forget()

def add_expenses_page():
    global add_expenses_frame, quantity_entry, source_entry
    add_expenses_frame = Frame(root, bg='#ABB2B9')
    add_expenses_frame_width = width * .35
    add_expenses_frame_height = height * .25
    add_expenses_frame.place(x=width*.35, y=height*.3, width=add_expenses_frame_width, height=add_expenses_frame_height)

    title_frame = Frame(add_expenses_frame, bg='#117A65')
    title_frame.place(x=0, y=0, width=add_expenses_frame_width, height=30)
    title = Label(title_frame, text='إضافة مصروفات', bg='#117A65', font=('tajawal', 12, 'bold'))
    title.pack()
    exit_btn = Button(title_frame, text='x', bg='red', fg='white', font=('tajawal', 20), bd=0, cursor='hand2', command=hide_add_expenses_page)
    exit_btn.place(x=add_expenses_frame_width*.92, y=0, width=add_expenses_frame_width*.08, height=30)

    quantity_lb = Label(add_expenses_frame, text='المبلغ', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    quantity_lb.place(x=add_expenses_frame_width*.7, y=add_expenses_frame_height*.2, width=add_expenses_frame_width*.3, height=add_expenses_frame_height*.1)
    quantity_entry = Entry(add_expenses_frame,  fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    quantity_entry.place(x=add_expenses_frame_width*.3, y=add_expenses_frame_height*.2, width=add_expenses_frame_width*.4, height=add_expenses_frame_height*.1)
    source_lb = Label(add_expenses_frame, text='مصدر الإنفاق', bg='#ABB2B9', fg='#117A65', font=('tajawal', 12, 'bold'))
    source_lb.place(x=add_expenses_frame_width*.7, y=add_expenses_frame_height*.4, width=add_expenses_frame_width*.3, height=add_expenses_frame_height*.1)
    source_entry = Entry(add_expenses_frame,  fg='#117A65', font=('tajawal', 12, 'bold'), bd=0, highlightbackground='#117A65', highlightcolor='#117A65', highlightthickness=2, justify=CENTER)
    source_entry.place(x=add_expenses_frame_width*.3, y=add_expenses_frame_height*.4, width=add_expenses_frame_width*.4, height=add_expenses_frame_height*.1)
    add_btn = Button(add_expenses_frame, text='حفظ', bg='#ABB2B9', fg='#117A65', bd=2, relief=SOLID, font=('tajawal', 12, 'bold'), cursor='hand2', command=add_expenses)
    add_btn.place(x=add_expenses_frame_width*.4, y=add_expenses_frame_height*.75, width=add_expenses_frame_width*.2, height=add_expenses_frame_height*.15)

def on_treeview_click(event):
    global item_data
    selected_item = expenses_table.selection()
    item_data = expenses_table.item(selected_item, 'values')
    row_id = expenses_table.identify_row(event.y)
    column_id = expenses_table.identify_column(event.x)
    if column_id == "#0":
        if row_id:
            operation_no = expenses_db.fetch_operation_no(item_data[3])
            operations_db.remove_operation(operation_no[0])
            expenses_db.remove_expenses(item_data[3])
        display_all()

#------------------ UpSide Frame ------------------
upside_frame = Frame(root, bg='#117A65')
def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()

upside_frame_width = int(width)
upside_frame_height = int(height * .05)
upside_frame.place(x=0, y=0, width=upside_frame_width, height=upside_frame_height)

title = Label(upside_frame, text='المصروفات', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

logo = Label(upside_frame, image=expenses_logo, bg='#117A65')
logo.place(x=upside_frame_width*.95, y=upside_frame_height*.1)

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.02, y=upside_frame_height*.1)


#--------------------- DownSide Frame -------------------------
downside_frame = Frame(root, bg='#117A65')
downside_frame_width = int(width)
downside_frame_height = int(height * .05)
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_btn = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_expenses_page)
add_btn.place(x=downside_frame_width*.95, y=downside_frame_height*.1)

#------------------ View Bills Frame -------------------------------
view_frame = Frame(root, bg='#ABB2B9')
view_frame_width = width
view_frame_height = height - upside_frame_height - downside_frame_height -60
view_frame.place(x=0, y=upside_frame_height, width=view_frame_width, height=view_frame_height)

Scroll_y = Scrollbar(view_frame, width=20, orient=VERTICAL)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
expenses_table = ttk.Treeview(view_frame,
                        columns=('date', 'source', 'quantity', 'expenses_no'),
                        yscrollcommand=Scroll_y.set)
expenses_table.place(x=0, y=0, width=view_frame_width-20, height=view_frame_height)
Scroll_y.pack(fill=Y, side=RIGHT)
Scroll_y.config(cursor='hand2', command=expenses_table.yview)

expenses_table.heading('date', text='التاريخ')
expenses_table.heading('source', text='مصدر الإنفاق')
expenses_table.heading('quantity', text='المبلغ')
expenses_table.heading('expenses_no', text='رقم العملية')
expenses_table.column('#0', width=int(view_frame_width*.05), anchor=CENTER)
expenses_table.column('date', width=int(view_frame_width*.15), anchor=CENTER)
expenses_table.column('source', width=int(view_frame_width*.35), anchor=CENTER)
expenses_table.column('quantity', width=int(view_frame_width*.3), anchor=CENTER)
expenses_table.column('expenses_no', width=int(view_frame_width*.1), anchor=CENTER)

expenses_table.bind('<ButtonRelease-1>', on_treeview_click)

display_all()

root.mainloop()
from tkinter import *
from tkinter import ttk
import os
from tkinter import messagebox
from subprocess import Popen
import json
from manager_databases.items_db import ItemsDatabase
from manager_databases.products_db import ProductsDatabase

root = Tk()
root.lift()
width = int(root.winfo_screenwidth())
height = int(root.winfo_screenheight())
root.state('zoomed')
root.title('Company Name')
root.config(bg='#ABB2B9')


#------------------------ Variables ------------------------------
search_icon = PhotoImage(file='images\\search_icon.png')
add_icon = PhotoImage(file='images\\add_icon.png')
back_icon = PhotoImage(file='images\\left_arrow.png')

name = StringVar()

items_db = ItemsDatabase('login_signup_page\\manager_options\\manager_databases\\items_db.db')
pro_db = ProductsDatabase('login_signup_page\\manager_options\\manager_databases\\products_db.db')


#------------------------ Functions -------------------------------
def get_data(e):
    selected_row = items_list.focus()
    data = items_list.item(selected_row)
    global row
    row = data['values']
    return row

def save(e):
    data = get_data(e)
    with open('data_file2.json', 'w') as wf:
        json.dump(data, wf)
    update_page()

def display_all():
    load1()
    items_list.delete(*items_list.get_children())
    for row in items_db.fetch():
        items_list.insert('', END, values=row)

def load1():
    global data, got_name, got_id
    with open('data_file2.json', 'r') as rf:
        if os.path.getsize('data_file2.json') != 0:
            data = json.load(rf)
            got_name, got_id= data
            got_id
            name.set(got_name)
            items_db.update(
                got_id, got_name
            )

def go_back():
    Popen(['python', 'login_signup_page\\manager_options.py'])
    quit()

#----------------------- Add Item Page -------------------------
def add_window():
    pro = Tk()
    pro_width = int(width*.2)
    pro_height = int(height*.15)
    pro.geometry(f'{pro_width}x{pro_height}+{int(width*.4)}+{int(height*.35)}')
    pro.title('Company Name')
    pro.config(bg='#ABB2B9')

    title = Label(pro, text='إضافة صنف', font=('tajawal', 12, 'bold'), bg='#117A65')
    title.pack(fill=X)

    name_lb = Label(pro, text='الصنف', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65')
    name_lb.place(x=pro_width*.8, y=pro_height*.3)
    global name_entry
    name_entry = Entry(pro, fg='#117A65', font=('tajawal', 12, 'bold'), textvariable=name, justify=CENTER)
    name_entry.place(x=pro_width*.1, y=pro_height*.3)

    add_btn = Button(pro, text='إضافة', font=('tajawal', 12, 'bold'), fg='#117A65', cursor='hand2', command=add)
    add_btn.place(x=pro_width*.25, y=pro_height*.7, width=pro_width*.5, height=pro_height*.2)

    pro.mainloop()


def add():
    if name_entry.get() == '':
        messagebox.showerror('خطأ', 'أدخل اسم الصنف')
    else:
        items_db.insert(name_entry.get())
        name.set('')
        display_all()

#--------------- Update Item Page --------------------------------
def update_page():
    pro = Tk()
    width = int(pro.winfo_screenwidth())
    height = int(pro.winfo_screenheight())
    pro_width = int(width*.2)
    pro_height = int(height*.15)
    pro.geometry(f'{pro_width}x{pro_height}+{int(width*.4)}+{int(height*.35)}')
    pro.title('Company Name')
    pro.config(bg='#ABB2B9')

    title = Label(pro, text='تعديل صنف', font=('tajawal', 12, 'bold'), bg='#117A65')
    title.pack(fill=X)

    global name
    name = StringVar()
    items_db = ItemsDatabase('login_signup_page\\manager_options\\manager_databases\\items_db.db')

    def delete():
        items_db.remove(got_id)
        display_all()

    def load():
        with open('data_file2.json', 'r') as rf:
            global data, got_name, got_id
            data = json.load(rf)
        if data != []:
            got_name, got_id = data
            name.set(got_name)
        
        return got_id, name
    load()

    def update():
        if name_entry.get() == '':
            messagebox.showerror('خطأ', 'يجب ملئ جميع الحقول')
        elif items_db.check_existence(name_entry.get()):
            messagebox.showerror('خطأ', 'هذا الصنف موجود بالفعل')
        items_db.update(got_id,
            name.set(name_entry.get()))
        pro_db.upadte_items(got_name, name_entry.get())
        return (got_id, name_entry.get())

    def save1():
        data = update()
        with open('data_file2.json', 'w') as wf:
            json.dump(data, wf)
        display_all()

    name_lb = Label(pro, text='الصنف', font=('tajawal', 12, 'bold'), bg='#ABB2B9', fg='#117A65')
    name_lb.place(x=pro_width*.8, y=35)
    global name_entry
    name_entry = Entry(pro, justify=CENTER, textvariable=name)
    name_entry.place(x=pro_width*.2, y=40, width=pro_width*.5)

    update_btn = Button(pro, text='تعديل', font=('tajawal', 9, 'bold'), fg='#117A65', cursor='hand2', command=save1)
    update_btn.place(x=pro_width*.58, y=pro_height*.7, width=pro_width*.2)
    remove_btn = Button(pro, text='حذف', font=('tajawal', 9, 'bold'), fg='red', cursor='hand2', command=delete)
    remove_btn.place(x=pro_width*.2, y=pro_height*.7, width=pro_width*.2)


#------------------------ UpSide Frame ----------------------------
upside_frame_height = 35
upside_frame_width = width
upside_frame = Frame(root, bg='#117A65')
upside_frame.pack(fill=X)

title = Label(upside_frame, text='الأصناف', bg='#117A65', font=('tajawal', 15, 'bold'))
title.pack()

back_btn = Button(upside_frame, image=back_icon, bg='#117A65', bd=0, cursor='hand2', command=go_back)
back_btn.place(x=upside_frame_width*.005, y=upside_frame_height*.15)
#-------------- DownSide Frame -------------------------------
downside_frame = Frame(root, bg='#117A65')
downside_frame_height = height*.12
downside_frame_width = width
downside_frame.place(x=0, y=height*.88, width=downside_frame_width, height=downside_frame_height)

add_button = Button(downside_frame, image=add_icon, bg='#117A65', bd=0, cursor='hand2', command=add_window)
add_button.place(x=downside_frame_width*.96, y=downside_frame_height*.05)

#------------------ View Frame ------------------------------
show_frame = Frame(root, bg='#ABB2B9')
show_frame_width = width
show_frame_height = height- upside_frame_height - downside_frame_height
show_frame.place(x=0, y=upside_frame_height, width=show_frame_width, height=show_frame_height)

scroll_y = Scrollbar(show_frame, orient=VERTICAL, width=20)
list = ttk.Style()
list.configure('Treeview', rowheight=40, font=('tajawal', 9, 'bold'))
items_list = ttk.Treeview(show_frame,
                            columns=('items', 'id'),
                            yscrollcommand=scroll_y.set)
items_list.place(x=0, y=0, width=show_frame_width-20, height=show_frame_height)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(cursor='hand2', command=items_list.yview)

items_list['show'] = 'headings'
items_list.heading('items', text='الصنف')
items_list.heading('id', text='id')
items_list.column('items', width=int(show_frame_width*.8), anchor=CENTER)
items_list.column('id', width=int(show_frame_width*.1), anchor=CENTER)

items_list.bind('<ButtonRelease-1>', save)
display_all()


root.mainloop()
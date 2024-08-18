from tkinter import *
from databases.master_db import Database
from databases.managers_db import ManagersDatabase
from databases.employees_db import EmployeesDatabase

root = Tk()
width = int(root.winfo_screenwidth())
height = int(root.winfo_screenheight())
root.state('zoomed')
root.title('Company Name')
root.config(bg='#ABB2B9')


#-------------------------- Variables ---------------------------------------
products_img = PhotoImage(file='images\\sections\\products.png')
items_img = PhotoImage(file='images\\sections\\items.png')
selling_bill_img = PhotoImage(file='images\\sections\\selling_bill.png')
buying_bill_img = PhotoImage(file='images\\sections\\buying_bill.png')

#---------------------------- Buttons --------------------------------------
products_btn = Button(root, text='الأصناف', image=items_img, compound=TOP, fg='#117A65', bg='#ABB2B9', cursor='hand2', bd=.5, relief='solid', font=('tajawal', 12, 'bold'))
products_btn.place(x=width*.2, y=height*.2, width=width*.2, height=height*.2)
types_btn = Button(root, text='المنتجات', image=products_img, compound=TOP, fg='#117A65', bg='#ABB2B9', cursor='hand2', bd=.5, relief='solid', font=('tajawal', 12, 'bold'))
types_btn.place(x=width*.6, y=height*.2, width=width*.2, height=height*.2)
sales_btn = Button(root, text='المشتريات', image=buying_bill_img, compound=TOP, fg='#117A65', bg='#ABB2B9', cursor='hand2', bd=.5, relief='solid', font=('tajawal', 12, 'bold'))
sales_btn.place(x=width*.2, y=height*.6, width=width*.2, height=height*.2)
buys_btn = Button(root, text='المبيعات', image=selling_bill_img, compound=TOP, fg='#117A65', bg='#ABB2B9', cursor='hand2', bd=.5, relief='solid', font=('tajawal', 12, 'bold'))
buys_btn.place(x=width*.6, y=height*.6, width=width*.2, height=height*.2)

root.mainloop()
from tkinter import *
from subprocess import Popen
from tkinter import messagebox
import getpass
from databases.master_db import Database
from databases.managers_db import ManagersDatabase
from databases.employees_db import EmployeesDatabase

root = Tk()
width = int(root.winfo_screenwidth() * .3)
height = int(root.winfo_screenheight() * .4)
x = int(root.winfo_screenwidth() * .35)
y = int(root.winfo_screenheight() * .2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.title('Company Name')
root.config(bg='#ABB2B9')
root.resizable(False, False)

#------------------- variables ---------------------------
db = Database('C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\login_signup_page\\databases\\Master.db')
man_db =ManagersDatabase('C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\login_signup_page\\databases\\managers_db.db')
emp_db = EmployeesDatabase('C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\login_signup_page\\databases\\employees_db.db')

man_options = 'login_signup_page\\manager_options.py'
emp_options = 'login_signup_page\\employee_options.py'

login_username = StringVar()
login_password = StringVar()
username = StringVar()
password = StringVar()
re_password = StringVar()

show_pass1 = IntVar(value=0)
show_pass2 = IntVar(value=0)
show_pass3 = IntVar(value=0)
show_pass4 = IntVar(value=0)
show_pass5 = IntVar(value=0)
show_pass6 = IntVar(value=0)
show_pass7 = IntVar(value=0)
show_pass8 = IntVar(value=0)
show_pass9 = IntVar(value=0)


#-------------------------- show and mask password -------------------------
def show1():
    if show_pass1.get() == 1:
        password_entry.config(show='')
    else:
        password_entry.config(show='*')
def show2():
    if show_pass2.get() == 1:
        re_password_entry.config(show='')
    else:
        re_password_entry.config(show='*')
def show3():
    if show_pass3.get() == 1:
        man_password_entry.config(show='')
    else:
        man_password_entry.config(show='*')
def show4():
    if show_pass4.get() == 1:
        man_repassword_entry.config(show='')
    else:
        man_repassword_entry.config(show='*')
def show5():
    if show_pass5.get() == 1:
        emp_password_entry.config(show='')
    else:
        emp_password_entry.config(show='*')
def show6():
    if show_pass6.get() == 1:
        emp_repassword_entry.config(show='')
    else:
        emp_repassword_entry.config(show='*')
def show7():
    if show_pass7.get() == 1:
        login_password_entry.config(show='')
    else:
        login_password_entry.config(show='*')
def show8():
    if show_pass8.get() == 1:
        master_pass_entry.config(show='')
    else:
        master_pass_entry.config(show='*')
def show9():
    if show_pass8.get() == 1:
        man_password_entry2.config(show='')
    else:
        man_password_entry2.config(show='*')


#------------------------ First Time Page -----------------------------------------
if(db.fetch() == []):
    width = int(root.winfo_screenwidth() * .3)
    height = int(root.winfo_screenheight() * .4)
    x = int(root.winfo_screenwidth() * .35)
    y = int(root.winfo_screenheight() * .2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.title('Company Name')
    root.config(bg='#ABB2B9')
    root.resizable(False, False)

    def add_master():
        if username_entry.get() == '' or password_entry.get() == '' or re_password_entry.get() == '':
            messagebox.showerror('خطأ', 'يجب ملئ كل الحقول')
        elif password_entry.get() != re_password_entry.get():
            messagebox.showerror('خطأ', 'كلمة السر مختلفة')
        elif len(password_entry.get()) < 8:
            messagebox.showerror('خطأ', 'كلمة السر يجب ألا تقل عن 8 أحرف')
        else:
            db.insert(
                username_entry.get(),
                password_entry.get()
            )
            man_db.insert(
                username_entry.get(),
                password_entry.get()
            )
            Popen(['python', man_options])
            quit()

    master_lb = Label(root, text='''سوق الجملة\nللأدوات المنزلية''', bg='#ABB2B9', fg='#117A65', font=('tajawal', 15, 'bold'), justify=CENTER)
    master_lb.place(x=width*.25, width=width*.5, height=height*.3)
    note_lb = Label(root, text='يرجى العلم أن كلمة السر المستخدمة سيتم طلبها عند إنشاء حساب لأي مدير', bg='#A3E4D7', fg='black', font=('tajawal', 9, 'bold'), bd=0, highlightbackground='#239B56', highlightthickness=.5)
    note_lb.place(x=width*.095, y=height*.3, width=width*.9, height=height*.1)

    username = Label(root, text='اسم المستخدم', bg='#ABB2B9', fg='#16A085', font=('tajawal', 12, 'bold'), justify=RIGHT)
    username.place(x=width*.6, y=height*.45, width=width*.4, height=height*.1)
    username_entry = Entry(root, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify=CENTER, textvariable=username)
    username_entry.place(x=width*.1, y=height*.47, width=width*.5)

    password = Label(root, text='كلمة السر', bg='#ABB2B9', fg='#16A085', font=('tajawal', 12, 'bold'), justify='right')
    password.place(x=width*.6, y=height*.55, width=width*.4, height=height*.1)
    password_entry = Entry(root, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*', justify=CENTER, textvariable=password)
    password_entry.place(x=width*.1, y=height*.57, width=width*.5)
    show1_frame = Frame(root, bg='#ABB2B9')
    show1_frame.place(x=width*.39, y=height*.635)
    show_btn = Checkbutton(show1_frame, bg='#ABB2B9', onvalue=1, offvalue=0, variable=show_pass1, cursor='hand2', command=show1)
    show_btn.pack(side=RIGHT)
    show1_lb = Label(show1_frame, text='إظهار كلمة المرور', bg='#ABB2B9', fg='#16A085', font=('tajawal', 9, 'bold'))
    show1_lb.pack(side=LEFT)

    re_password = Label(root, text='أعد إدخال كلمة السر', bg='#ABB2B9', fg='#16A085', font=('tajawal', 12, 'bold'), justify='right')
    re_password.place(x=width*.6, y=height*.71, width=width*.4)
    re_password_entry = Entry(root, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*', justify=CENTER, textvariable=re_password)
    re_password_entry.place(x=width*.1, y=height*.71, width=width*.5)
    show2_frame = Frame(root, bg='#ABB2B9')
    show2_frame.place(x=width*.39, y=height*.785)
    show_btn = Checkbutton(show2_frame, bg='#ABB2B9', onvalue=1, offvalue=0, variable=show_pass2, cursor='hand2', command=show2)
    show_btn.pack(side=RIGHT)
    show1_lb = Label(show2_frame, text='إظهار كلمة المرور', bg='#ABB2B9', fg='#16A085', font=('tajawal', 9, 'bold'))
    show1_lb.pack(side=LEFT)

    left_arrow = PhotoImage(file='images\\left_arrow.png')
    signup_btn = Button(root, text='إنشاء حساب', image=left_arrow, compound=LEFT, bg='#ABB2B9', font=('tajawal', 9, 'bold'), cursor='hand2', command=add_master)
    signup_btn.place(x=width*.35, y=height*.88, width=width*.3, height=height*.1)



else:
#------------------- SignUp Options --------------------------------------------
    def signup_page():
        root.geometry(f'{int(width*1.61)}x{height}')
        signup_frame = Frame(root, bg='white')
        signup_frame_width = (width*.6)-15
        signup_frame_height = height-10
        signup_frame.place(x=width, y=5, width=signup_frame_width, height=signup_frame_height)

        zoomout_btn = Button(root, text='<', cursor='hand2', command=zoomout, font=('tajawal', 9, 'bold'))
        zoomout_btn.place(x=width*1.61-15, y=0, width=15, height=height)

        title = Label(signup_frame, text='اختر منصبك', bg='white', font=('tajawal', 12, 'bold'))
        title.pack()

        manager_btn= Button(signup_frame, text='مدير', image=manager_image, compound=TOP, bg='white', font=('tajawal', 9, 'bold'), cursor='hand2', command=manager_signup)
        manager_btn.place(x=signup_frame_width*.25, y=signup_frame_height*.1, width=signup_frame_width*.5, height=signup_frame_height*.3)
        employees_btn = Button(signup_frame, text='موظف', image=employees_image, compound=TOP, bg='white', font=('tajawal', 9, 'bold'), cursor='hand2', command=employee_signup)
        employees_btn.place(x=signup_frame_width*.25, y=signup_frame_height*.6, width=signup_frame_width*.5, height=signup_frame_height*.3)

#----------------------------- Manager SignUp Page ----------------------------------
    def manager_signup():
        root.geometry(f'{int(width*1.61)}x{height}')
        signup_frame = Frame(root, bg='white')
        signup_frame_width = (width*.6)-15
        signup_frame_height = height-10
        signup_frame.place(x=width, y=5, width=signup_frame_width, height=signup_frame_height)

        zoomout_btn = Button(root, text='<', cursor='hand2', command=zoomout, font=('tajawal', 9, 'bold'))
        zoomout_btn.place(x=width*1.61-15, y=0, width=15, height=height)

        title = Label(signup_frame, text='إنشاء حساب مدير', bg='white', font=('tajawal', 12, 'bold'))
        title.pack()

        man_username = Label(signup_frame, text='اسم المستخدم', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        man_username.place(x=signup_frame_width*.6, y=signup_frame_height*.1, width=signup_frame_width*.4, height=signup_frame_height*.1)
        global man_username_entry
        man_username_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), textvariable=man_username)
        man_username_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.12, width=signup_frame_width*.5)
        
        man_password = Label(signup_frame, text='كلمة السر', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        man_password.place(x=signup_frame_width*.6, y=signup_frame_height*.2, width=signup_frame_width*.4, height=signup_frame_height*.1)
        global man_password_entry
        man_password_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        man_password_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.22, width=signup_frame_width*.5)

        show3_frame = Frame(signup_frame, bg='white')
        show3_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.29)
        show3_btn = Checkbutton(show3_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass3, cursor='hand2', command=show3)
        show3_btn.pack(side=RIGHT)
        show3_lb = Label(show3_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show3_lb.pack(side=LEFT)
        
        man_repassword = Label(signup_frame, text='إعادة إدخال كلمة\nالسر', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        man_repassword.place(x=signup_frame_width*.6, y=signup_frame_height*.37, width=signup_frame_width*.4, height=signup_frame_height*.2)
        global man_repassword_entry
        man_repassword_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        man_repassword_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.44, width=signup_frame_width*.5)

        show4_frame = Frame(signup_frame, bg='white')
        show4_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.52)
        show4_btn = Checkbutton(show4_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass4, cursor='hand2', command=show4)
        show4_btn.pack(side=RIGHT)
        show4_lb = Label(show4_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show4_lb.pack(side=LEFT)

        master_pass = Label(signup_frame, text='كلمة سر المالك', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        master_pass.place(x=signup_frame_width*.6, y=signup_frame_height*.59, width=signup_frame_width*.4, height=signup_frame_height*.2)
        global master_pass_entry
        master_pass_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        master_pass_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.64, width=signup_frame_width*.5)

        show8_frame = Frame(signup_frame, bg='white')
        show8_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.72)
        show8_btn = Checkbutton(show8_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass8, cursor='hand2', command=show8)
        show8_btn.pack(side=RIGHT)
        show8_lb = Label(show8_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show8_lb.pack(side=LEFT)

        signup_btn1 = Button(signup_frame, text='إنشاء حساب', bg='#16A085', fg='white', font=('tajawal', 9, 'bold'), cursor='hand2', command=new_manager)
        signup_btn1.place(x=signup_frame_width*.15, y=signup_frame_height*.85, width=signup_frame_width*.7)

    def new_manager():
        if (man_db.check_exist(
            man_username_entry.get()
            ) or
            emp_db.check_exist(
            man_username_entry.get()
            )):
            messagebox.showerror('خطأ' ,'اسم المستخدم موجود بالفعل')
        elif len(man_password_entry.get()) < 8:
            messagebox.showerror('خطأ', 'كلمة المرور يجب ألا تقل عن 8 أحرف')
        elif man_password_entry.get() != man_repassword_entry.get():
            messagebox.showerror('خطأ' ,'كلمة السر مختلفة')
        elif not(db.check_pass(master_pass_entry.get())):
            messagebox.showerror('خطأ', 'كلمة سر المالك غير صحيحة')
        else:
            man_db.insert(
                man_username_entry.get(),
                man_password_entry.get()
                )
            Popen(['python', man_options])
            quit()

#-------------------------- Employee SignUp Page -------------------------------
    def employee_signup():
        root.geometry(f'{int(width*1.61)}x{height}')
        signup_frame = Frame(root, bg='white')
        signup_frame_width = (width*.6)-15
        signup_frame_height = height-10
        signup_frame.place(x=width, y=5, width=signup_frame_width, height=signup_frame_height)

        zoomout_btn = Button(root, text='<', cursor='hand2', command=zoomout, font=('tajawal', 9, 'bold'))
        zoomout_btn.place(x=width*1.61-15, y=0, width=15, height=height)

        title = Label(signup_frame, text='إنشاء حساب موظف', bg='white', font=('tajawal', 12, 'bold'))
        title.pack()

        emp_username = Label(signup_frame, text='اسم المستخدم', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        emp_username.place(x=signup_frame_width*.6, y=signup_frame_height*.1, width=signup_frame_width*.4, height=signup_frame_height*.1)
        global emp_username_entry
        emp_username_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        emp_username_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.12, width=signup_frame_width*.5)
        
        emp_password = Label(signup_frame, text='كلمة السر', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        emp_password.place(x=signup_frame_width*.6, y=signup_frame_height*.2, width=signup_frame_width*.4, height=signup_frame_height*.1)
        global emp_password_entry
        emp_password_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        emp_password_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.22, width=signup_frame_width*.5)

        show5_frame = Frame(signup_frame, bg='white')
        show5_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.29)
        show5_btn = Checkbutton(show5_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass5, cursor='hand2', command=show5)
        show5_btn.pack(side=RIGHT)
        show5_lb = Label(show5_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show5_lb.pack(side=LEFT)
        
        emp_repassword = Label(signup_frame, text='إعادة إدخال كلمة\nالسر', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        emp_repassword.place(x=signup_frame_width*.6, y=signup_frame_height*.37, width=signup_frame_width*.4, height=signup_frame_height*.2)
        global emp_repassword_entry
        emp_repassword_entry = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        emp_repassword_entry.place(x=signup_frame_width*.1, y=signup_frame_height*.44, width=signup_frame_width*.5)

        show6_frame = Frame(signup_frame, bg='white')
        show6_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.52)
        show6_btn = Checkbutton(show6_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass6, cursor='hand2', command=show6)
        show6_btn.pack(side=RIGHT)
        show6_lb = Label(show6_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show6_lb.pack(side=LEFT)

        man_pass = Label(signup_frame, text='كلمة سر المالك', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        man_pass.place(x=signup_frame_width*.6, y=signup_frame_height*.59, width=signup_frame_width*.4, height=signup_frame_height*.2)
        global man_password_entry2
        man_password_entry2 = Entry(signup_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), show='*')
        man_password_entry2.place(x=signup_frame_width*.1, y=signup_frame_height*.64, width=signup_frame_width*.5)

        show9_frame = Frame(signup_frame, bg='white')
        show9_frame.place(x=signup_frame_width*.22, y=signup_frame_height*.72)
        show9_btn = Checkbutton(show9_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass3, cursor='hand2', command=show9)
        show9_btn.pack(side=RIGHT)
        show9_lb = Label(show9_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show9_lb.pack(side=LEFT)

        signup_btn1 = Button(signup_frame, text='إنشاء حساب', bg='#16A085', fg='white', font=('tajawal', 9, 'bold'), cursor='hand2', command=new_employee)
        signup_btn1.place(x=signup_frame_width*.15, y=signup_frame_height*.85, width=signup_frame_width*.7)

    def new_employee():
        if ((emp_db.check_exist(emp_username_entry.get()))
            or (man_db.check_exist(emp_username_entry.get()))):
            messagebox.showerror('خطأ', 'اسم المستخدم موجود بالفعل')
        elif len(emp_password_entry.get()) < 8:
            messagebox.showerror('خطأ', 'كلمة المرور يجب ألا تقل عن 8 أحرف')
        elif emp_password_entry.get() != emp_repassword_entry.get():
            messagebox.showerror('خطأ' ,'كلمة السر مختلفة')
        elif not(man_db.check_pass(man_password_entry2.get())):
            messagebox.showerror('خطأ', 'كلمة سر المدير غير صحيحة')
        else:
            emp_db.insert(
                emp_username_entry.get(),
                emp_password_entry.get()
                )
            Popen(['python', emp_options])
            quit()

#------------------------------- Login Page --------------------------------            
    def login():
        if (man_db.check(
            login_username_entry.get(),
            login_password_entry.get()
            )):
            Popen(['python', man_options])
            quit()
        elif (emp_db.check(
            login_username_entry.get(),
            login_password_entry.get()
            )):
            Popen(['python', emp_options])
            quit()
        else:
            messagebox.showerror('خطأ', 'اسم المستخدم أو كلمة المرور غير صحيح')


    def login_page():
        root.geometry(f'{int(width*1.61)}x{height}')
        login_frame = Frame(root, bg='white')
        login_frame_width = (width*.6)-15
        login_frame_height = height-10
        login_frame.place(x=width, y=5, width=login_frame_width, height=login_frame_height)

        zoomout_btn = Button(root, text='<', cursor='hand2', command=zoomout, font=('tajawal', 9, 'bold'))
        zoomout_btn.place(x=width*1.61-15, y=0, width=15, height=height)

        title = Label(login_frame, text='تسجيل الدخول', bg='white', font=('tajawal', 12, 'bold'))
        title.pack()

        login_username = Label(login_frame, text='اسم المستخدم', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify=RIGHT)
        login_username.place(x=login_frame_width*.6, y=login_frame_height*.1, width=login_frame_width*.4, height=login_frame_height*.1)
        global login_username_entry
        login_username_entry = Entry(login_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), textvariable=login_username)
        login_username_entry.place(x=login_frame_width*.1, y=login_frame_height*.12, width=login_frame_width*.5)

        login_password = Label(login_frame, text='كلمة السر', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), justify='right')
        login_password.place(x=login_frame_width*.6, y=login_frame_height*.3, width=login_frame_width*.4, height=login_frame_height*.1)
        global login_password_entry 
        login_password_entry= Entry(login_frame, bg='white', fg='#16A085', font=('tajawal', 9, 'bold'), textvariable=login_password, show='*')
        login_password_entry.place(x=login_frame_width*.1, y=login_frame_height*.32, width=login_frame_width*.5)

        show7_frame = Frame(login_frame, bg='white')
        show7_frame.place(x=login_frame_width*.22, y=height*.38)
        show7_btn = Checkbutton(show7_frame, bg='white', onvalue=1, offvalue=0, variable=show_pass7, cursor='hand2', command=show7)
        show7_btn.pack(side=RIGHT)
        show7_lb = Label(show7_frame, text='إظهار كلمة المرور', bg='white', fg='#16A085', font=('tajawal', 9, 'bold'))
        show7_lb.pack(side=LEFT)

        login_btn1 = Button(login_frame, text='تسجيل الدخول', bg='#16A085', fg='white', font=('tajawal', 9, 'bold'), cursor='hand2', command=login)
        login_btn1.place(x=login_frame_width*.15, y=login_frame_height*.6, width=login_frame_width*.7)

    def zoomout():
        root.geometry(f'{width}x{height}+{x}+{y}')


#---------------- Images --------------------------
    image = PhotoImage(file='C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\images\\login_image.png')
    main_image = Label(root, bg='#ABB2B9', image=image, width=width, height=int(height*.5))
    main_image.place(x=0, y=0)

    login_logo = PhotoImage(file='C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\images\\login_logo.png')
    signup_logo = PhotoImage(file='C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\images\\signup_logo.png')

    manager_image = PhotoImage(file='C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\images\\manager.png')
    employees_image = PhotoImage(file='C:\\Users\\Abdulrahman\\Desktop\\First_Practical_Project\\images\\employees.png')

#----------------- Buttons ---------------------------
    login_btn = Button(root, text='تسجيل الدخول', image=login_logo, compound=TOP, bg='#ABB2B9', font=('tajawal', 9, 'bold'), cursor='hand2', command=login_page)
    login_btn.place(x=width*.6, y=height*.6, width=width*.3, height=height*.3)

    signup_btn = Button(root, text='إنشاء حساب', image=signup_logo, compound=TOP, bg='#ABB2B9', font=('tajawal', 9, 'bold'), cursor='hand2', command=signup_page)
    signup_btn.place(x=width*.1, y=height*.6, width=width*.3, height=height*.3)

root.mainloop()
from tkinter import *
from PIL import Image, ImageTk
import pymysql
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

expenditure = []
debit_amount = []
mnth1 = []
amnt1 = []
amnt2 = []
cnt: int = 0

# home = 'urHomeDomain'
# newlogin = 'urnewlogin'
# edit = 'ureditWindow'
# profile = 'urprofile'
# delWin = 'urdeleteWindow'
# track_money = 'trackMoney'
# mnth = 'monthTracker'
# frgt = 'forgetWindow'

def login():
    global userID
    try:
        connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    except:
        messagebox.showwarning("Not Connected", "Start MySQL Server First")
    else:
        Email = User.get()
        Password = Pass.get()
        cur = connection.cursor()
        if Email == "" and Password == "":
            messagebox.showerror("Incomplete Data", "All fields are required")
        #elif Email == "" or Password == "":
            #messagebox.showerror("Incomplete Data", "Username or Password not provided")
        else:
            # messagebox.showinfo("Connected", "Connected Successfully to database")
            query = "SELECT emailid , password FROM login"
            cur.execute(query)
            for (email, pas) in cur:
                if Email == email and Password == pas:
                    login = True
                    break
                else:
                    login = False
            userID = (Email.split('@')[0])
            if login == True:
                newWindow()
                messagebox.showinfo("Logged in", "Logged in successfully!!!")
            elif login == False:
                messagebox.showerror("Warning!", "Wrong Username or Password")
            connection.close()


def forgot_password():
    global frgt
    if (forgot_password_window.secQue2.get() == "" or forgot_password_window.secAns2.get() == "" or
            forgot_password_window.newPassword.get() == "" or forgot_password_window.cnfnewPassword.get() == ""):
        messagebox.showerror("Error", "All fields required", parent=frgt)
    elif (forgot_password_window.newPassword.get() != forgot_password_window.cnfnewPassword.get()):
        messagebox.showerror("Error", "New Password and Confirm New Password must be same", parent=frgt)
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
            cur = connection.cursor()
            query = "SELECT * FROM login WHERE emailid=%s and security_que=%s and security_ans=%s"
            cur.execute(query, (User.get(), forgot_password_window.secQue2.get(), forgot_password_window.secAns2.get()))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please select correct security question/answer", parent=frgt)
            else:
                query2 = "UPDATE login SET password=%s WHERE emailid=%s"
                cur.execute(query2, (forgot_password_window.newPassword.get(), User.get()))
                connection.commit()
                connection.commit()
                messagebox.showinfo("Success",
                                    "Your password has been reset successfully!!\nPlease login with new password",
                                    parent=frgt)
                clear_resetpassword_window()
                frgt.destroy()
                User.delete(0, END)
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}")


def forgot_password_window():
    global frgt
    if User.get() == "":
        messagebox.showerror("Error", "Please enter Username")
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
            cur = connection.cursor()
            cur.execute("SELECT * FROM login WHERE emailid=%s", User.get())
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter valid username")
            else:
                connection.close()
                frgt = Toplevel(root)
                frgt.title("Forgot Password")
                frgt.geometry("450x500+450+150")
                frgt.config(bg='gray')
                frgt.focus_force()

                frame1 = Frame(frgt, bd=2, relief=SUNKEN)
                frame1 = LabelFrame(frgt)
                frame1.place(x=25, y=5, width=400, height=480)

                title = Label(frame1, text="Forgot Password", font=("times", 22, "bold"), bg='white', fg="red").place(x=0, y=0, relwidth=1)

                secquel2 = Label(frame1, text="Security Question", font=('arial', 15, 'bold'), fg='black').place(x=80,y=70)
                forgot_password_window.secQue2 = ttk.Combobox(frame1, font=('caliber', 13), width=22)
                forgot_password_window.secQue2['values'] = ('', 'Your first pet name', 'Your birth place', 'Your best friend name', 'Your First School Name')
                forgot_password_window.secQue2.place(x=80, y=100)

                secansl2 = Label(frame1, text="Security Answer", font=('arial', 15, 'bold'), fg='black').place(x=80,y=150)
                forgot_password_window.secAns2 = Entry(frame1, width=20, font=('caliber', 15),
                                                       highlightbackground='black', highlightthickness=1, bg='lightgray')
                forgot_password_window.secAns2.place(x=80, y=180)

                newPasswordl = Label(frame1, text="New Password", font=('arial', 15, 'bold'), fg='black').place(x=80,y=230)
                forgot_password_window.newPassword = Entry(frame1, width=20, font=('caliber', 15),
                                                           highlightbackground='black',highlightthickness=1, bg='lightgray', show="*")
                forgot_password_window.newPassword.place(x=80, y=260)

                cnfnewPasswordl = Label(frame1, text="Confirm New Password", font=('arial', 15, 'bold'),
                                        fg='black').place(x=80, y=310)
                forgot_password_window.cnfnewPassword = Entry(frame1, width=20, font=('caliber', 15),
                                                              highlightbackground='black', highlightthickness=1, bg='lightgray', show="*")
                forgot_password_window.cnfnewPassword.place(x=80, y=340)

                chng_btn = Button(frame1, text="RESET PASSWORD", bg='green', fg='white', font=('times', 15, 'bold'),
                                  command=forgot_password).place(x=80, y=420)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}")


def clear_resetpassword_window():
    forgot_password_window.secQue2.delete(0, END)
    forgot_password_window.secAns2.delete(0, END)
    forgot_password_window.newPassword.delete(0, END)
    forgot_password_window.cnfnewPassword.delete(0, END)


def clearNewlogin():
    newLogin.first_name.delete(0, END)
    newLogin.last_name.delete(0, END)
    newLogin.EmailID.delete(0, END)
    newLogin.Occupation.delete(0, END)
    newLogin.mobnum.delete(0, END)
    newLogin.set_password.delete(0, END)
    newLogin.cnf_password.delete(0, END)
    newLogin.secQue.delete(0, END)
    newLogin.secAns.delete(0, END)


def create():
    connection = pymysql.connect(host="localhost", user="root", password="17ankita#", db="database1")
    if (newLogin.first_name.get()=="" or newLogin.last_name.get()=="" or newLogin.EmailID.get()=="" or
            newLogin.Occupation.get()=="" or newLogin.mobnum.get()=="" or newLogin.set_password.get()=="" or
            newLogin.cnf_password.get()=="" or newLogin.secQue.get()=="" or newLogin.secAns.get()==""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    elif newLogin.set_password.get() != newLogin.cnf_password.get():
        messagebox.showerror("Error", "Password and Confirm password should be same...")
    else:
        try:
            cur = connection.cursor()
            cur.execute("SELECT * FROM login WHERE emailid=%s", User.get())
            row = cur.fetchone()
            if row!=None:
                messagebox.showerror("User already exist","User already exist please try another Email-ID")
            else:
                sqlinsert = "INSERT INTO login(first_name,last_name,emailid,occupation,mobile_number,password,security_que,security_ans)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(sqlinsert,
                            (newLogin.first_name.get(), newLogin.last_name.get(),newLogin.EmailID.get(), newLogin.Occupation.get(),
                             newLogin.mobnum.get(), newLogin.set_password.get(), newLogin.secQue.get(), newLogin.secAns.get()))
                connection.commit()
                connection.close()
                messagebox.showinfo("Data Inserted", "Data Saved Successfully")
                clearNewlogin()
        except Exception as es:
            messagebox.showerror("Error",f"Error due to : {str(es)}")


def back():
    global newlogin
    newlogin.withdraw()
    root.deiconify()


def addCredit():
    credit = newWindow.credit_entry.get()
    date = newWindow.date_entry.get()
    credit_mode = newWindow.mode_of_credit.get()

    if (newWindow.date_entry.get() == "" or newWindow.credit_entry.get() == "" or newWindow.mode_of_credit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        newWindow.txt_box1.insert(END,
                                  "       " + date + "\t\t       " + credit + "\t\t                 " + credit_mode + "\n")

        credit_table()
        clearCredit()


def addDebit():
    date = newWindow.date_entry.get()
    expenditure = newWindow.item.get()
    deposit = newWindow.deposit_entry.get()
    deposit_mode = newWindow.mode_of_deposit.get()

    if (newWindow.date_entry.get() == "" or newWindow.item.get() == "" or newWindow.deposit_entry.get() == "" or
            newWindow.mode_of_deposit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")

    else:
        newWindow.txt_box2.insert(END, " " + date + "\t   " + expenditure + "\t\t       " + deposit +
                                  "\t\t" + deposit_mode + "\n")

        debit_table()
        clearDebit()


def credit_table():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    if (newWindow.date_entry.get() == "" or newWindow.credit_entry.get() == "" or newWindow.mode_of_credit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        cur = connection.cursor()
        insert_credit = "INSERT INTO credit(Date_of_Credit,Amount_Credited,Mode_of_Credit,emailid)VALUES(%s,%s,%s,%s)"
        cur.execute(insert_credit,
                    (newWindow.date_entry.get(), newWindow.credit_entry.get(), newWindow.mode_of_credit.get(),
                     User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Data Inserted", "Credit data inserted to table successfully")


def debit_table():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    if (newWindow.date_entry.get() == "" or newWindow.item.get() == "" or newWindow.deposit_entry.get() == "" or
            newWindow.mode_of_deposit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        cur = connection.cursor()
        insert_debit = "INSERT INTO debit(Date_of_Debit,Expenditure,Amount_Debited,Mode_of_Debit,emailid)VALUES(%s,%s,%s,%s,%s)"
        cur.execute(insert_debit,
                    (newWindow.date_entry.get(), newWindow.item.get(), newWindow.deposit_entry.get(),
                     newWindow.mode_of_deposit.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Data Inserted", "Debit data inserted to table successfully")


def printTotal():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query1 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s"
    cur.execute(query1, (User.get()))
    result1 = cur.fetchall()

    query2 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s"
    cur.execute(query2, (User.get()))
    result2 = cur.fetchall()

    result = result1[0][0] - result2[0][0]
    newWindow.balance_entry.insert(0, result)


def clearCredit():
    newWindow.date_entry.delete(0, END)
    newWindow.credit_entry.delete(0, END)
    newWindow.mode_of_credit.delete(0, END)


def clearDebit():
    newWindow.date_entry.delete(0, END)
    newWindow.item.delete(0, END)
    newWindow.deposit_entry.delete(0, END)
    newWindow.mode_of_deposit.delete(0, END)


def clearShow():
    newWindow.balance_entry.delete(0, END)


def clearLogin():
    User.delete(0, END)
    Pass.delete(0, END)


def exitWindow():
    global home
    home.withdraw()
    root.deiconify()
    clearLogin()
    messagebox.showinfo("Logged Out", "Logged out Successfully!!!")


def delete_debit():
    res = messagebox.askquestion("Delete Debit", "Do you really want to delete debit data?")
    if res == 'yes':
        connection = pymysql.connect(host="localhost", user="root", password="17ankita#", db="database1")
        cur = connection.cursor()
        if (deleteWindow.entry4.get() == "" or deleteWindow.entry3.get() == "" or deleteWindow.entry5.get() == ""):
            messagebox.showerror("No Debit Data", "No debit data selected to delete")
        else:
            query = "DELETE FROM debit WHERE emailid=%s AND Expenditure=%s AND Date_of_Debit=%s AND Amount_Debited=%s"
            cur.execute(query,
                        (User.get(), deleteWindow.entry4.get(), deleteWindow.entry3.get(), deleteWindow.entry5.get()))
            connection.commit()
            messagebox.showinfo("Debit Deleted", "Debit Transaction deleted successfully")
            clear_deleteDebit()
            clear_display_debit()
            display_debit()
    else:
        messagebox.showinfo("Delete Data", "Debit Data not deleted")


def delete_credit():
    res = messagebox.askquestion("Delete Credit", "Do you really want to delete credit data?")
    if res == 'yes':
        connection = pymysql.connect(host="localhost", user="root", password="17ankita#", db="database1")
        cur = connection.cursor()
        if (deleteWindow.entry1.get() == "" or deleteWindow.entry2.get() == ""):
            messagebox.showerror("No Credit data", "No credit data selected to delete")
        else:
            query = "DELETE FROM credit WHERE emailid=%s AND Date_of_Credit=%s AND Amount_Credited=%s"
            cur.execute(query, (User.get(), deleteWindow.entry1.get(), deleteWindow.entry2.get()))
            connection.commit()
            messagebox.showinfo("Credit Deleted", "Credit Transaction deleted successfully")
            clear_deleteCredit()
            clear_display_credit()
            display_credit()
    else:
        messagebox.showinfo("Delete Data", "Credit Data not deleted")


def clear_deleteDebit():
    deleteWindow.entry4.delete(0, END)
    deleteWindow.entry3.delete(0, END)
    deleteWindow.entry5.delete(0, END)


def clear_deleteCredit():
    deleteWindow.entry1.delete(0, END)
    deleteWindow.entry2.delete(0, END)


def display_debit():
    clear_display_debit()
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query1 = "SELECT * FROM debit WHERE emailid = %s order by date(Date_of_Debit)"
    cur.execute(query1, (User.get()))
    result1 = cur.fetchall()
    if len(result1) != 0:
        for rows in result1:
            date1 = str(rows[0])
            expenditure1 = rows[1]
            amount1 = str(rows[2])
            mode = rows[3]
            newWindow.txt_box2.insert(END, " " + date1 + "\t   " + expenditure1 + "\t\t       " + amount1 +
                                      "\t\t" + mode + "\n")
        messagebox.showinfo("Debit Records Entered", "Debit Records Entered successfully")
    else:
        messagebox.showerror("No Data", "Debit History not available")
    connection.commit()
    connection.close()


def display_credit():
    clear_display_credit()
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query2 = "SELECT * FROM credit WHERE emailid = %s order by date(Date_of_Credit)"
    cur.execute(query2, (User.get()))
    result2 = cur.fetchall()
    if len(result2) != 0:
        for rows in result2:
            date2 = str(rows[0])
            amount2 = str(rows[1])
            mode = rows[2]
            newWindow.txt_box1.insert(END,
                                      "       " + date2 + "\t\t       " + amount2 + "\t\t                 " + mode + "\n")
        messagebox.showinfo("Credit Records Entered", "Credit Records Entered successfully")
    else:
        messagebox.showerror("No Data", "Credit History not available")
    connection.commit()
    connection.close()


def clear_display_credit():
    newWindow.txt_box1.delete("1.0", END)


def clear_display_debit():
    newWindow.txt_box2.delete("1.0", END)


def new_details():
    clear_display_debit()
    clear_display_credit()


# ------ DELETE TRANSACTION -----------------------------------------------------

def back_delete():
    global delWin
    delWin.withdraw()
    home.deiconify()


# ********************** DELETE WINDOW ********************

def deleteWindow():
    global delWin
    delWin = Toplevel(root)
    delWin.title("Delete Transaction")
    delWin.geometry("740x730+0+30")
    delWin.config(bg='skyblue')
    delWin.resizable(False, False)

    frame = Frame(delWin, bd=6, relief=SUNKEN)
    frame.place(x=20, y=40, width=650, height=650)

    # --------------- Frame1 ------------------------------------------------------------------
    frame1 = Frame(delWin, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(delWin, text="Credit Details", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame1.place(x=70, y=90, width=560, height=230)

    lab1 = Label(frame1, text="Date of Credit      :", font=('arial', 15))
    lab1.place(x=50, y=20)
    deleteWindow.entry1 = DateEntry(frame1, font=('arial', 15), date_pattern='yyyy-mm-dd')
    deleteWindow.entry1.place(x=250, y=20)

    lab2 = Label(frame1, text="Amount Credited   :", font=('arial', 15))
    lab2.place(x=50, y=60)
    deleteWindow.entry2 = Entry(frame1, bd=3, bg='#ffff99', font=('arial', 15))
    deleteWindow.entry2.place(x=250, y=60)

    image = Image.open("delete.jpeg")
    image = image.resize((130, 90), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image)
    label = Label(newlogin, image=test)
    label.image = test

    back_btn = Button(frame1, width=100, height=60, command=delete_credit, compound=LEFT, bg='red', relief=RAISED, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=185, y=110)

    # --------------- Frame2 ------------------------------------------------------------------

    frame2 = Frame(delWin, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(delWin, text="Debit Details", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame2.place(x=70, y=350, width=560, height=270)

    lab3 = Label(frame2, text="Date of Debit       :", font=('arial', 15))
    lab3.place(x=50, y=20)
    deleteWindow.entry3 = DateEntry(frame2, font=('arial', 15), date_pattern='yyyy-mm-dd')
    deleteWindow.entry3.place(x=250, y=20)

    lab4 = Label(frame2, text="Expenditure         :", font=('arial', 15))
    lab4.place(x=50, y=60)
    deleteWindow.entry4 = ttk.Combobox(frame2, font=('arial', 15), width=18, justify='left')
    deleteWindow.entry4['values'] = (
        '', 'EMI', 'Maintainence', 'Shopping', 'Food', 'Health', 'Entertainment', 'Travelling', 'Other')
    deleteWindow.entry4.place(x=250, y=60)

    lab5 = Label(frame2, text="Amount Debited   :", font=('arial', 15))
    lab5.place(x=50, y=100)
    deleteWindow.entry5 = Entry(frame2, bd=3, bg='#ffff99', font=('arial', 15))
    deleteWindow.entry5.place(x=250, y=100)

    back_btn = Button(frame2, width=100, height=60, command=delete_debit, compound=LEFT, bg='red', relief=RAISED, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=185, y=155)

    image12 = Image.open("back1.jpeg")
    image12 = image12.resize((65, 45), Image.ANTIALIAS)
    test12 = ImageTk.PhotoImage(image12)
    label12 = Label(newlogin, image=test12)
    label12.image = test12

    back_btn = Button(delWin, width=45, height=16, command=back_delete, compound=LEFT, relief=FLAT, bd=5,
                      image=test12, cursor="hand2")
    back_btn.place(x=690, y=10)


def back_last_update():
    global last
    last.withdraw()
    home.deiconify()


# --------------------- last update------------------------------------------------------
def last_update():
    global last
    last = Toplevel(root)
    last.title("Last Transaction")
    last.geometry("740x730+0+30")
    last.config(bg="skyblue")
    last.resizable(False, False)

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    frame = Frame(last, bd=6, relief=SUNKEN)
    frame.place(x=20, y=40, width=650, height=650)

    # ********************* FRAME 1 CREDIT TRANSACTION *************************

    frame1 = Frame(last, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(last, text="Credit Transaction", bd=6, font=('Times', 17, 'bold'), fg='darkblue')
    frame1.place(x=70, y=80, width=560, height=260)

    lab1 = Label(frame1, text="Date                     :", font=('arial', 15))
    lab1.place(x=40, y=30)
    entry1 = Entry(frame1, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry1.place(x=245, y=30)

    lab2 = Label(frame1, text="Amount Credited    :", font=('arial', 15))
    lab2.place(x=40, y=80)
    entry2 = Entry(frame1, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry2.place(x=245, y=80)

    lab3 = Label(frame1, text="Mode of Payment   : ", font=('arial', 15))
    lab3.place(x=40, y=130)
    entry3 = Entry(frame1, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry3.place(x=245, y=130)

    query2 = "SELECT Date_of_Credit, Amount_Credited, Mode_of_Credit FROM credit WHERE emailid=%s"
    cur.execute(query2, User.get())
    result2 = cur.fetchall()
    for i in result2:
        date1 = i[0]
        amt1 = i[1]
        mode1 = i[2]

    entry1.insert(0, date1)
    entry2.insert(0, amt1)
    entry3.insert(0, mode1)

    # ********************* FRAME 2 DEBIT TRANSACTION *************************

    frame2 = Frame(last, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(last, text="Debit Transaction", bd=6, font=('Times', 17, 'bold'), fg='darkblue')
    frame2.place(x=70, y=370, width=560, height=280)

    lab4 = Label(frame2, text="Date                     :", font=('arial', 15))
    lab4.place(x=40, y=30)
    entry4 = Entry(frame2, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry4.place(x=245, y=30)

    lab5 = Label(frame2, text="Amount Debited     :", font=('arial', 15))
    lab5.place(x=40, y=80)
    entry5 = Entry(frame2, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry5.place(x=245, y=80)

    lab6 = Label(frame2, text="Expenditure           :", font=('arial', 15))
    lab6.place(x=40, y=130)
    entry6 = Entry(frame2, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry6.place(x=245, y=130)

    lab7 = Label(frame2, text="Mode of Payment   : ", font=('arial', 15))
    lab7.place(x=40, y=180)
    entry7 = Entry(frame2, font=('arial', 15), bd=5, bg='#ffff99', relief=SUNKEN)
    entry7.place(x=245, y=180)

    query1 = "SELECT Date_of_Debit, Expenditure, Amount_Debited, Mode_of_Debit FROM debit WHERE emailid=%s"
    cur.execute(query1, User.get())
    result1 = cur.fetchall()
    for j in result1:
        date2 = j[0]
        exp = j[1]
        amt2 = j[2]
        mode2 = j[3]

    entry4.insert(0, date2)
    entry5.insert(0, amt2)
    entry6.insert(0, exp)
    entry7.insert(0, mode2)

    image = Image.open("back1.jpeg")
    image = image.resize((65, 45), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image)
    label = Label(newlogin, image=test)
    label.image = test

    back_btn = Button(last, width=45, height=16, command=back_last_update, compound=LEFT, relief=FLAT, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=690, y=10)


def back_monthTracker():
    global mnth
    mnth.withdraw()
    home.deiconify()


def monthTracker():
    global mnth
    mnth = Toplevel(root)
    mnth.title("MONTHLY TRACKER")
    mnth.geometry("740x730+0+30")
    mnth.config(bg="skyblue")
    mnth.resizable(False,False)

    frame = Frame(mnth, bd=6, relief=SUNKEN)
    frame.place(x=20, y=40, width=650, height=650)

    # **************************** FRAME 1 ********************************

    frame1 = Frame(mnth, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(mnth, text="Compare Monthly", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame1.place(x=60, y=60, width=580, height=400)

    lab1 = Label(frame1, text="Month 1", font=('arial', 15))
    lab1.place(x=75, y=15)

    monthTracker.ref1 = ttk.Combobox(frame1, font=('arial', 15))
    monthTracker.ref1['values'] = (
        '', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December')
    monthTracker.ref1.place(x=10, y=50)

    lab2 = Label(frame1, text="Month 2", font=('arial', 15))
    lab2.place(x=375, y=15)

    monthTracker.ref2 = ttk.Combobox(frame1, font=('arial', 15))
    monthTracker.ref2['values'] = (
        '', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December')
    monthTracker.ref2.place(x=290, y=50)

    cmpr_btn1 = Button(frame1, text="COMPARE", font=("Times", 15, "bold"), fg="white", bg='#009999',
                       activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                       command=compare, cursor="hand2").place(x=215, y=90)

    lab3 = Label(frame1, text="Month 1", font=('arial', 15))
    lab3.place(x=180, y=150)

    lab4 = Label(frame1, text="Month 2", font=('arial', 15))
    lab4.place(x=380, y=150)

    lab5 = Label(frame1, text="Credited\nAmount", font=('arial', 15))
    lab5.place(x=10, y=190)

    lab6 = Label(frame1, text="Debited\nAmount", font=('arial', 15))
    lab6.place(x=10, y=250)

    monthTracker.entry1 = Entry(frame1, font=('arial', 15), bd=3, width=15)
    monthTracker.entry1.place(x=140, y=205)

    monthTracker.entry2 = Entry(frame1, font=('arial', 15), bd=3, width=15)
    monthTracker.entry2.place(x=340, y=205)

    monthTracker.entry3 = Entry(frame1, font=('arial', 15), bd=3, width=15)
    monthTracker.entry3.place(x=140, y=265)

    monthTracker.entry4 = Entry(frame1, font=('arial', 15), bd=3, width=15)
    monthTracker.entry4.place(x=340, y=265)

    clr_btn1 = Button(frame1, text="CLEAR", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                      command=clear_monthTracker, cursor="hand2").place(x=215, y=305)


    # ********************** FRAME 2 *******************************

    frame2 = Frame(mnth, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(mnth, text="Graphical Representation Yearly", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame2.place(x=60, y=480, width=580, height=175)

    lab = Label(frame2, text="Plot Graph:", font=('arial', 15))
    lab.place(x=80, y=25)

    monthTracker.opt_box = ttk.Combobox(frame2, font=('arial', 17))
    monthTracker.opt_box['values'] = ('', 'Bar Graph', 'Line Graph', 'Stacked Bar Graph')
    monthTracker.opt_box.place(x=200, y=25)

    btn1 = Button(frame2, text="MONTHLY HISTORY", font=('Times', 15, 'bold'), fg="white", bg='#009999',
                  activebackground='#669999', width=18, height=1, relief=RAISED, bd=5,
                  command=data_barChart2, cursor="hand2").place(x=170, y=80)

    image = Image.open("back1.jpeg")
    image = image.resize((65, 45), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image)
    label = Label(newlogin, image=test)
    label.image = test

    back_btn = Button(mnth, width=45, height=16, command=back_monthTracker, compound=LEFT, relief=FLAT, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=690, y=10)


def compare():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s AND MONTHNAME(Date_of_Credit)=%s"
    cur.execute(query1, (User.get(), monthTracker.ref1.get()))
    result1 = cur.fetchall()
    monthTracker.entry1.insert(0, result1[0][0])

    query2 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s AND MONTHNAME(Date_of_Credit)=%s"
    cur.execute(query2, (User.get(), monthTracker.ref2.get()))
    result2 = cur.fetchall()
    monthTracker.entry2.insert(0, result2[0][0])

    query3 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s AND MONTHNAME(Date_of_Debit)=%s"
    cur.execute(query3, (User.get(), monthTracker.ref1.get()))
    result3 = cur.fetchall()
    monthTracker.entry3.insert(0, result3[0][0])

    query4 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s AND MONTHNAME(Date_of_Debit)=%s"
    cur.execute(query4, (User.get(), monthTracker.ref2.get()))
    result4 = cur.fetchall()
    monthTracker.entry4.insert(0, result4[0][0])


def clear_monthTracker():
    monthTracker.entry1.delete(0, END)
    monthTracker.entry2.delete(0, END)
    monthTracker.entry3.delete(0, END)
    monthTracker.entry4.delete(0, END)
    monthTracker.ref1.delete(0, END)
    monthTracker.ref2.delete(0, END)


def data_barChart2():
    global mnth1, amnt1, amnt2

    mnth1 *= 0  # clearing list
    amnt1 *= 0  # clearing list
    amnt2 *= 0  # clearing list

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    # **************** QUERY FOR MONTH ********************************

    query1 = "SELECT MONTHNAME(Date_of_Debit) AS 'Month Name' FROM debit WHERE emailid=%s ORDER BY MONTH(Date_of_Debit)"
    cur.execute(query1, User.get())
    result1 = cur.fetchall()
    for m in result1:
        if m[0] not in mnth1:
            mnth1.append(m[0])

    # ************************* QUERY FOR SUM OF AMOUNT DEBITED *******************************

    query2 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid = %s GROUP BY MONTHNAME(Date_of_Debit) ORDER BY MONTH(Date_of_Debit)"
    cur.execute(query2, User.get())
    result2 = cur.fetchall()
    for i in result2:
        amnt1.append(i[0])

    # *********************************** QUERY FOR SUM OF AMOUNT CREDITED ***********************************

    query3 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid = %s GROUP BY MONTHNAME(Date_of_Credit) ORDER BY MONTH(Date_of_Credit)"
    cur.execute(query3, User.get())
    result3 = cur.fetchall()
    for j in result3:
        amnt2.append(j[0])

    if monthTracker.opt_box.get() == "Bar Graph":
        bar1 = np.arange(len(mnth1))
        bar2 = [i + 0.4 for i in bar1]
        plt.xticks(bar1 + 0.4 / 2, mnth1)
        plt.bar(bar2, amnt1, 0.4, label="Debit")
        plt.bar(bar1, amnt2, 0.4, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    elif monthTracker.opt_box.get() == "Line Graph":
        plt.plot(mnth1, amnt1, label="Debit")
        plt.plot(mnth1, amnt2, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    elif monthTracker.opt_box.get() == "Stacked Bar Graph":
        plt.bar(mnth1, amnt1, 0.4, label="Debit")
        plt.bar(mnth1, amnt2, 0.4, bottom=amnt1, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    else:
        messagebox.showerror("Error", "Select proper option..!!!")


# ************************ HISTORY WINDOW ***************************************************

def view():
    if trackMoney.ref6.get() == 'Bar Chart':
        barChart()
    elif trackMoney.ref6.get() == 'Pie Chart':
        pieChart()
    else:
        messagebox.showerror("Error", "Please select proper option")


def barChart():
    global expenditure, debit_amount
    expenditure *= 0
    debit_amount *= 0

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT Expenditure, SUM(Amount_Debited) FROM debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s group by expenditure"
    cur.execute(query1, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    for i in result1:
        expenditure.append(i[0])
        debit_amount.append(i[1])

    plt.style.use('bmh')
    plt.xlabel('Expenditure', fontsize=15)
    plt.ylabel('Amount', fontsize=15)
    plt.bar(expenditure, debit_amount, 0.4)
    plt.title("Debit Amount V/S Expenditure")
    plt.show()
    # expenditure.clear()
    # debit_amount.clear()


def pieChart():
    global expenditure, debit_amount
    expenditure *= 0
    debit_amount *= 0

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT Expenditure, SUM(Amount_Debited) FROM debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s group by expenditure"
    cur.execute(query1, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    for i in result1:
        expenditure.append(i[0])
        debit_amount.append(i[1])

    plt.style.use('bmh')
    plt.pie(debit_amount, labels=expenditure, radius=1.2, autopct='%0.01f%%', shadow=True)
    plt.title("Debit Amount V/S Expenditure")
    plt.show()

    # expenditure.clear()
    # debit_amount.clear()


def track1():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "SELECT SUM(Amount_Credited) from credit WHERE emailid=%s AND Date_of_Credit BETWEEN %s AND %s"
    cur.execute(query, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    trackMoney.ref3.insert(0, result1)

    query = "SELECT SUM(Amount_Debited) from debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s"
    cur.execute(query, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result2 = cur.fetchall()
    trackMoney.ref4.insert(0, result2)

    result3 = result1[0][0] - result2[0][0]
    trackMoney.ref5.insert(0, result3)


def reset():
    trackMoney.ref3.delete(0, END)
    trackMoney.ref4.delete(0, END)
    trackMoney.ref5.delete(0, END)


def back_trackMoney():
    global track_money
    track_money.withdraw()
    home.deiconify()


def trackMoney():
    global track_money
    track_money = Toplevel(root)
    track_money.title("TRACK MONEY")
    track_money.geometry("740x730+0+30")
    # track_money.geometry("750x730+450+20")
    track_money.config(bg="skyblue")
    track_money.resizable(False, False)

    frame = Frame(track_money, bd=6, relief=SUNKEN)
    frame.place(x=20, y=20, width=650, height=680)

    # ******************* FRAME 1 ******************************

    frame1 = Frame(track_money, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(track_money, text="Date Entry", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame1.place(x=60, y=45, width=565, height=180)

    trackMoney.label1 = Label(frame1, text="Starting Date    :", font=("arial", 15))
    trackMoney.label1.place(x=70, y=10)
    trackMoney.ref1 = DateEntry(frame1, font=("arial", 15), date_pattern="yyyy-mm-dd")
    trackMoney.ref1.place(x=250, y=10)

    trackMoney.label2 = Label(frame1, text="Ending Date      :", font=("arial", 15))
    trackMoney.label2.place(x=70, y=50)
    trackMoney.ref2 = DateEntry(frame1, font=("arial", 15), date_pattern="yyyy-mm-dd")
    trackMoney.ref2.place(x=250, y=50)

    show_btn = Button(frame1, text="SHOW", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                      command=track1, cursor="hand2").place(x=220, y=100)

    # ************************* FRAME 2 *********************************

    frame2 = Frame(track_money, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(track_money, text="Details", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame2.place(x=60, y=235, width=565, height=250)

    trackMoney.lab3 = Label(frame2, text='Total money Earn        :', font=('arial', 15))
    trackMoney.lab3.place(x=40, y=20)
    trackMoney.ref3 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=15)
    trackMoney.ref3.place(x=280, y=20)

    trackMoney.lab4 = Label(frame2, text='Total money spent       :', font=('arial', 15))
    trackMoney.lab4.place(x=40, y=70)
    trackMoney.ref4 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=15)
    trackMoney.ref4.place(x=280, y=70)

    trackMoney.lab5 = Label(frame2, text='Total money available   :', font=('arial', 15))
    trackMoney.lab5.place(x=40, y=120)
    trackMoney.ref5 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=15)
    trackMoney.ref5.place(x=280, y=120)

    reset_btn = Button(frame2, text="CLEAR", font=("Times", 15, "bold"), fg="white", bg='#009999',
                       activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                       command=reset, cursor="hand2").place(x=220, y=170)

    # ******************** FRAME 3 ********************************

    frame3 = Frame(track_money, bd=2, relief=SUNKEN)
    frame3 = LabelFrame(track_money, text="Graphical Representation", bd=6, font=('Times', 16, 'bold'), fg='darkblue')
    frame3.place(x=60, y=495, width=565, height=180)

    trackMoney.lab6 = Label(frame3, text="Plot Graph  :", font=('arial', 16))
    trackMoney.lab6.place(x=70, y=25)

    trackMoney.ref6 = ttk.Combobox(frame3, font=('arial', 17))
    trackMoney.ref6['values'] = ('', 'Bar Chart', 'Pie Chart')
    trackMoney.ref6.place(x=200, y=25)

    view_btn = Button(frame3, text="VIEW", font=('Times', 15, 'bold'), fg='white', bg='#009999',
                      activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                      command=view, cursor="hand2").place(x=220, y=75)

    image = Image.open("back1.jpeg")
    image = image.resize((65, 45), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image)
    label = Label(newlogin, image=test)
    label.image = test

    back_btn = Button(track_money, width=45, height=16, command=back_trackMoney, compound=LEFT, relief=FLAT, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=690, y=10)


# *********************** EDIT WINDOW **********************

def My_data():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "Select first_name from login where emailid = %s"
    cur.execute(query, User.get())
    res1 = cur.fetchone()
    Profile.first_name.insert(0, res1)

    cur = connection.cursor()
    query = "Select last_name from login where emailid = %s"
    cur.execute(query, User.get())
    res2 = cur.fetchone()
    Profile.last_name.insert(0, res2)

    cur = connection.cursor()
    query = "Select occupation from login where emailid = %s"
    cur.execute(query, User.get())
    res3 = cur.fetchone()
    Profile.Occupation.insert(0, res3)

    cur = connection.cursor()
    query = "Select mobile_number from login where emailid = %s"
    cur.execute(query, User.get())
    res4 = cur.fetchone()
    Profile.mob_no.insert(0, res4)

    cur = connection.cursor()
    query = "Select emailid from login where emailid = %s"
    cur.execute(query, User.get())
    res5 = cur.fetchone()
    Profile.EmailID.insert(0, res5)


def clear_update_data():
    Profile.ref1.delete(0, END)
    Profile.ref2.delete(0, END)


def clear_update_field():
    Profile.first_name.delete(0, END)
    Profile.last_name.delete(0, END)
    Profile.Occupation.delete(0, END)
    Profile.mob_no.delete(0, END)
    Profile.EmailID.delete(0, END)


def update():
    if Profile.ref1.get() == "" and Profile.ref2.get() == "":
        messagebox.showerror("Error", "Please enter field & data to update")

    elif Profile.ref1.get() == "" or Profile.ref2.get() == "":
        messagebox.showerror("Error", "Enter data to update")

    else:
        connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
        if Profile.ref1.get() == 'first_name':
            cur = connection.cursor()
            query = "UPDATE login set first_name = %s where emailid =%s"
            cur.execute(query, (Profile.ref2.get(), User.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Updated", "First Name Updated Successfully")

        elif Profile.ref1.get() == 'last_name':
            cur = connection.cursor()
            query = "UPDATE login set last_name = %s where emailid =%s"
            cur.execute(query, (Profile.ref2.get(), User.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Updated", "Last Name Updated Successfully")

        elif Profile.ref1.get() == 'occupation':
            cur = connection.cursor()
            query = "UPDATE login set occupation = %s where emailid =%s"
            cur.execute(query, (Profile.ref2.get(), User.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Updated", "Occupation Updated Successfully")

        elif Profile.ref1.get() == 'mobile_number':
            cur = connection.cursor()
            query = "UPDATE login set mobile_number = %s where emailid =%s"
            cur.execute(query, (Profile.ref2.get(), User.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Updated", "Mobile No Updated Successfully")

        else:
            cur = connection.cursor()
            query = "UPDATE login set password = %s where emailid =%s"
            cur.execute(query, (Profile.ref2.get(), User.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Updated", "Password Updated Successfully")

        clear_update_data()
        clear_update_field()

        My_data()


# ************************ PROFILE WINDOW ********************

def back_update():
    global profile
    profile.withdraw()
    home.deiconify()


def Profile():
    global profile
    profile = Toplevel(root)
    profile.title("PROFILE PAGE")
    profile.geometry("740x730+450+30")
    profile.config(bg="skyblue")
    profile.resizable(False, False)

    frame = Frame(profile, bd=6, relief=SUNKEN)
    frame.place(x=20, y=30, width=650, height=670)

    # ******************** FRAME 1 ************************

    f1 = Frame(profile, bd=4, relief=SUNKEN)
    f1 = LabelFrame(profile, bd=4, font=('arial', 14, 'bold'))
    f1.place(x=70, y=60, width=560, height=390)

    image4 = Image.open("userface.png")
    image4 = image4.resize((140, 120), Image.ANTIALIAS)
    test4 = ImageTk.PhotoImage(image4)
    label4 = Label(profile, image=test4)
    label4.image = test4
    label4.place(x=140, y=65)

    something_1 = Label(f1, text="Personal Data", fg='darkblue', font=('arial', 25, 'bold'))
    something_1.place(x=210, y=45)

    first = Label(f1, text="First Name        :", font=('arial', 16), fg='black').place(x=50, y=145)
    Profile.first_name = Entry(f1, width=20, font=('caliber', 16), highlightbackground='black', bg='#ffff99',
                               highlightthickness=1)
    Profile.first_name.place(x=240, y=150)

    last = Label(f1, text="Last Name        :", font=('arial', 16), fg='black').place(x=50, y=185)
    Profile.last_name = Entry(f1, width=20, font=('caliber', 16), highlightbackground='black', bg='#ffff99',
                              highlightthickness=1)
    Profile.last_name.place(x=240, y=190)

    occ = Label(f1, text="Occupation       :", font=('arial', 16), fg='black').place(x=50, y=225)
    Profile.Occupation = Entry(f1, width=20, font=('caliber', 16), highlightbackground='black', bg='#ffff99',
                               highlightthickness=1)
    Profile.Occupation.place(x=240, y=230)

    mob_no = Label(f1, text="Mobile Number  :", font=('arial', 16), fg='black').place(x=50, y=265)
    Profile.mob_no = Entry(f1, width=20, font=('caliber', 16), highlightbackground='black', bg='#ffff99',
                           highlightthickness=1)
    Profile.mob_no.place(x=240, y=270)

    EmailID = Label(f1, text="Email-ID            :", font=('arial', 16), fg='black').place(x=50, y=305)
    Profile.EmailID = Entry(f1, width=20, font=('caliber', 16), highlightbackground='black', bg='#ffff99',
                            highlightthickness=1)
    Profile.EmailID.place(x=240, y=310)

    My_data()

    # ************************ FRAME 2 **************************

    f2 = Frame(profile, bd=4, relief=SUNKEN)
    f2 = LabelFrame(profile, text="Update Data", bd=4, font=('arial', 14, 'bold'), fg='darkblue')
    f2.place(x=70, y=460, width=560, height=215)

    Profile.lab1 = Label(f2, text='Update Field        :', font=('arial', 15))
    Profile.lab1.place(x=40, y=20)
    Profile.ref1 = ttk.Combobox(f2, font=("arial", 17), width=16)
    Profile.ref1['values'] = ('', 'first_name', 'last_name', 'occupation', 'mobile_number', 'password')
    Profile.ref1.place(x=250, y=20)

    Profile.lab2 = Label(f2, text='New data             :', font=('arial', 15))
    Profile.lab2.place(x=40, y=70)
    Profile.ref2 = Entry(f2, font=("arial", 15), bd=2, bg='#ffff99', width=20)
    Profile.ref2.place(x=250, y=70)

    show_btn = Button(f2, text="UPDATE", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                      command=update, cursor="hand2").place(x=180, y=130)

    image = Image.open("back1.jpeg")
    image = image.resize((65, 45), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image)
    label = Label(newlogin, image=test)
    label.image = test

    back_btn = Button(profile, width=45, height=16, command=back_update, compound=LEFT, relief=FLAT, bd=5,
                      image=test, cursor="hand2")
    back_btn.place(x=690, y=10)


# ************************ EXPENSE TRACKER MAIN WINDOW *********************************************************

def newWindow():
    global userID, home
    root.withdraw()  # closes the login window
    home = Toplevel(root)
    home.title("Main Window:: Expense Tracker")
    home.geometry("1500x750+15+0")
    home.configure(background="#cce6ff")  # "#08a3d2"
    home.resizable(False, False)

    # **************MENU BAR******************************
    my_menu = Menu(home)
    home.config(menu=my_menu)

    # ******************** EDIT MENU ******************************

    profile = Menu(my_menu, font="Times 15")
    my_menu.add_cascade(label="Profile", menu=profile)
    profile.add_command(label="Edit", command=Profile)
    profile.add_command(label="Logout", command=exitWindow)

    # ************** FILE MENU *******************************

    fileMenu = Menu(my_menu, font="Times 15 ")
    my_menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Transaction", command=new_details)
    fileMenu.add_command(label="Delete Transaction", command=deleteWindow)
    fileMenu.add_command(label="Display Credit Transaction", command=display_credit)
    fileMenu.add_command(label="Display Debit Transaction", command=display_debit)
    fileMenu.add_command(label="View Last Transaction", command=last_update)

    # ***************** HISTORY ***********************************

    track = Menu(my_menu, font="Times 15")
    my_menu.add_cascade(label="History", menu=track)
    track.add_command(label="Track Transaction", command=trackMoney)
    track.add_command(label="Track Monthly", command=monthTracker)

    # *************** GETTING NAME OF USER ************************

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    cur.execute("SELECT first_name, last_name FROM login WHERE emailid=%s", User.get())
    result = cur.fetchall()

    name = result[0][0] + "  " + result[0][1]

    name_label = Label(home, text=name.upper(), font=('times', 16, 'bold'), bg='#cce6ff')
    name_label.place(x=82,y=12)

    img = Image.open("userface.png")
    img = img.resize((65, 55), Image.ANTIALIAS)
    tst = ImageTk.PhotoImage(img)
    label4 = Label(home, image=tst, bg='#cce6ff')
    label4.image = tst
    label4.place(x=15, y=-3)

    # *******************FRAME 1 *********************************

    frame1 = Frame(home, bd=2, relief=SUNKEN)
    frame1.place(x=20, y=55, width=650, height=440)

    title1 = Label(frame1, text="Expenditure Info", font=("times new roman", 24, "underline"), bg="#666699",
                   fg="white", width=10, height=1).place(x=0, y=0, relwidth=1)

    # --------------- date entry ----------------------------------

    date_label = Label(frame1, text="Date                      : ", font=("times", 18), fg="black").place(x=40, y=60)
    newWindow.date_entry = DateEntry(frame1, font=("arial", 18), width=20, date_pattern='yyyy-mm-dd')
    newWindow.date_entry.place(x=270, y=60)

    # --------------- Credited Amount --------------------------------------
    credit_label = Label(frame1, text="Amount Credited  : ", font=("times", 18), fg="black").place(x=40, y=110)
    newWindow.credit_entry = Entry(frame1, font=("arial", 18), width=21, relief=SUNKEN)
    newWindow.credit_entry.place(x=270, y=110)

    # ---------------- Mode of Credit ------------------------------

    mode_of_credit = Label(frame1, text="Mode of Credit     : ", font=("times", 18), fg="black").place(x=40, y=160)
    newWindow.mode_of_credit = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.mode_of_credit['values'] = ('', 'Cash', 'Debit Card', 'Net Banking', 'UPI', 'Other')
    newWindow.mode_of_credit.place(x=270, y=160)

    # -------------- Money Spend on ----------------------------------------
    item_label = Label(frame1, text="Money Spend on  : ", font=("times", 18), fg="black").place(x=40, y=210)
    newWindow.item = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.item['values'] = (
        '', 'EMI', 'Maintainence', 'Shopping', 'Food', 'Health', 'Entertainment', 'Travelling', 'Other')
    newWindow.item.place(x=270, y=210)

    # -------------- Deposited Amount --------------------------------------------------------
    deposit_label = Label(frame1, text="Amount Debited  : ", font=("times", 18), fg="black").place(x=40, y=260)
    newWindow.deposit_entry = Entry(frame1, font=("arial", 18), width=21, relief=SUNKEN)
    newWindow.deposit_entry.place(x=270, y=260)

    # ------------- Mode of Deposit ---------------------------------------------

    mode_of_deposit = Label(frame1, text="Mode of Debit     :", font=("times", 18), fg="black").place(x=40, y=310)
    newWindow.mode_of_deposit = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.mode_of_deposit['values'] = ('', 'Cash', 'Debit Card', 'Net Banking', 'UPI', 'Other')
    newWindow.mode_of_deposit.place(x=270, y=310)

    # -------------------------- Add Button -------------------------------------

    add_btn1 = Button(frame1, text="ADD DEBIT DETAILS", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=19, height=1, relief=RAISED, bd=5,
                      command=addDebit, cursor="hand2").place(x=350, y=380)

    add_btn2 = Button(frame1, text="ADD CREDIT DETAILS", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=19, height=1, relief=RAISED, bd=5,
                      command=addCredit, cursor="hand2").place(x=50, y=380)

    # ***********************FRAME 2************************************************

    frame2 = Frame(home, bd=2, relief=SUNKEN)
    frame2.place(x=20, y=515, width=650, height=220)

    title2 = Label(frame2, text="Details", font=("times new roman", 24, "underline"), bg="#666699",
                   fg="white", width=10, height=1).place(x=0, y=0, relwidth=1)

    # ----------------------- Balance -----------------------------------------

    balance_label = Label(frame2, text="Total Balance   :", font=("times", 20), fg="black").place(x=80, y=75)
    newWindow.balance_entry = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=15)
    newWindow.balance_entry.place(x=300, y=75)

    # ------------------------ Show Button --------------------------------------

    show_btn = Button(frame2, text="SHOW", font=("Times", 15, "bold"), fg="white", bg='#009999',
                      activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                      command=printTotal, cursor="hand2").place(x=155, y=145)

    reset_btn = Button(frame2, text="CLEAR", font=("Times", 15, "bold"), fg="white", bg='#009999',
                       activebackground='#669999', width=9, height=1, relief=RAISED, bd=5,
                       command=clearShow, cursor="hand2").place(x=350, y=145)

    frame = Frame(home, bd=2, relief=SUNKEN)
    frame.place(x=685, y=17, width=800, height=720)

    # **************************FRAME 3 ******************************************

    frame3 = Frame(home, bd=2, relief=SUNKEN)
    frame3 = LabelFrame(home, text="Credit Details", bd=6, font=('arial', 14, 'bold'))
    frame3.place(x=700, y=20, width=780, height=340)

    # ---------------------- Headings -------------------------------------------

    heading_label1 = Label(frame3, font=("times", 18),
                           text="          Date                     Amount Credited                        Mode of Credit").place(x=20, y=10)

    newWindow.txt_box1 = Text(frame3, width=52, height=8, font=("times", 20))
    newWindow.txt_box1.place(x=20, y=40)

    scrlbar1 = ttk.Scrollbar(frame3, command=newWindow.txt_box1.yview)
    scrlbar1.place(relx=0.98, rely=0.94, relheight=0.8, anchor='se')
    newWindow.txt_box1.configure(yscrollcommand=scrlbar1.set)

    # ************************* Frame 4 ******************************************

    frame4 = Frame(home, bd=2, relief=SUNKEN)
    frame4 = LabelFrame(home, text="Debit Details", bd=6, font=('arial', 14, 'bold'))
    frame4.place(x=700, y=375, width=780, height=355)

    heading_label2 = Label(frame4, font=("times", 18),
                           text="    Date                Expenditure         Amount Debited        Mode of Payment").place(x=20, y=5)

    newWindow.txt_box2 = Text(frame4, width=52, height=9, font=("times", 20))
    newWindow.txt_box2.place(x=20, y=35)

    scrlbar2 = ttk.Scrollbar(frame4, command=newWindow.txt_box2.yview)
    scrlbar2.place(relx=0.98, rely=0.11, relheight=0.86, anchor='ne')
    newWindow.txt_box2.configure(yscrollcommand=scrlbar2.set)


# ************************* NEW LOGIN **********************************************************************

def newLogin():
    global userID, home, newlogin
    root.withdraw()  # close login page
    newlogin = Toplevel(root)
    newlogin.title("NEW REGISTRATION")
    newlogin.geometry('1500x750+10+0')
    newlogin.config(bg='white')
    newlogin.focus_force()
    newlogin.resizable(True, True)

    # ------------------------ BACKGROUND COLORS -----------------------------------------------------

    left_label = Label(newlogin, bg='#08a3d2', bd=0)
    left_label.place(x=0, y=0, relheight=1, width=750)

    right_label = Label(newlogin, bg='#031f3c', bd=0)
    right_label.place(x=750, y=0, relwidth=1, relheight=1)

    # -------------------------- MAIN FRAME -----------------------------------------------

    frame1 = Frame(newlogin, bg='white')
    frame1 = LabelFrame(newlogin, bg='white', bd=8, font=('arial', 14, 'bold'))
    frame1.place(x=230, y=50, width=1000, height=650)

    image4 = Image.open("newloginface.jpeg")
    image4 = image4.resize((180, 125), Image.ANTIALIAS)
    test4 = ImageTk.PhotoImage(image4)
    label4 = Label(frame1, image=test4)
    label4.image = test4
    label4.place(x=170, y=50)

    something_1 = Label(frame1, text="USER DETAILS", font=('times', 30, 'bold', 'underline'), bg="white", fg="#08a3d2")
    something_1.place(x=400, y=90)

    first = Label(frame1, text="First Name", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=50, y=200)
    newLogin.first_name = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                                highlightthickness=1, bg='lightgray')
    newLogin.first_name.place(x=50, y=230)

    last = Label(frame1, text="Last Name", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=350, y=200)
    newLogin.last_name = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                               highlightthickness=1, bg='lightgray')
    newLogin.last_name.place(x=350, y=230)

    Email = Label(frame1, text="Email-ID/Username", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=650,y=200)
    newLogin.EmailID = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                             highlightthickness=1, bg='lightgray')
    newLogin.EmailID.place(x=650, y=230)

    occ = Label(frame1, text="Occupation", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=200, y=280)
    newLogin.Occupation = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                                highlightthickness=1, bg='lightgray')
    newLogin.Occupation.place(x=200, y=310)

    mobnum = Label(frame1, text="Mobile Number", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=540,y=280)
    newLogin.mobnum = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                            highlightthickness=1,bg='lightgray')
    newLogin.mobnum.place(x=540, y=310)

    secquel = Label(frame1, text="Security Question", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=200, y=360)
    newLogin.secQue = ttk.Combobox(frame1, font=('caliber', 17), width=19)
    newLogin.secQue['values'] = ('', 'Your first pet name', 'Your birth place', 'Your best friend name', 'Your First School Name')
    newLogin.secQue.place(x=200, y=390)

    secansl = Label(frame1, text="Security Answer", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=540,y=360)
    newLogin.secAns = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                            highlightthickness=1,bg='lightgray')
    newLogin.secAns.place(x=540, y=390)

    set_pass = Label(frame1, text="Set Password", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=200,y=440)
    newLogin.set_password = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                                  highlightthickness=1, show='*', bg='lightgray')
    newLogin.set_password.place(x=200, y=470)

    cnf_password = Label(frame1, text="Confirm Password", font=('arial', 18, 'bold'), bg='white', fg='black').place(x=540, y=440)
    newLogin.cnf_password = Entry(frame1, width=20, font=('caliber', 17), highlightbackground='black',
                                  highlightthickness=1, show='*', bg='lightgray')
    newLogin.cnf_password.place(x=540, y=470)

    image10 = Image.open("save.jpeg")
    image10 = image10.resize((120, 80), Image.ANTIALIAS)
    test10 = ImageTk.PhotoImage(image10)
    label10 = Label(newlogin, image=test10)
    label10.image = test10

    save = Button(frame1, width=105, height=60, bg='blue', command=create, compound=LEFT, relief=RAISED, bd=5,
                  image=test10, cursor="hand2")
    save.place(x=320, y=530)

    image9 = Image.open("back.jpeg")
    image9 = image9.resize((130, 80), Image.ANTIALIAS)
    test9 = ImageTk.PhotoImage(image9)
    label9 = Label(newlogin, image=test9)
    label9.image = test9

    back_btn = Button(frame1, width=100, height=60, bg='gray', command=back, compound=LEFT, relief=RAISED, bd=5,
                      image=test9, cursor="hand2")
    back_btn.place(x=550, y=530)


# ************************** LOGIN PAGE ****************************************

root = Tk()
root.title("LOGIN PAGE")
root.geometry("1500x750+10+0")
root.focus_force()
root.resizable(False, False)

image1 = Image.open("login2.jpeg")
image1 = image1.resize((1500, 750), Image.ANTIALIAS)
test1 = ImageTk.PhotoImage(image1)
label1 = Label(root, image=test1)
label1.image = test1
label1.place(x=0, y=0)

site1 = Label(root, text='MONEY MANAGER', font=('Times', 44, 'bold'), fg="darkblue", bg="white")
site1.place(x=490, y=2)

username = Label(root, text="Username    :", font=('arial', 15, 'bold'), bg='#a1998e', fg='black').place(x=880, y=390)
User = Entry(root, width=27, font=('caliber', 15), bd=4, highlightbackground='black', highlightthickness=1)
User.place(x=1030, y=390)

password = Label(root, text="Password    :", font=('arial', 15, 'bold'), bg='#a1998e', fg='black').place(x=880, y=440)
Pass = Entry(root, width=27, font=('caliber', 15), bd=4, highlightbackground='black', highlightthickness=1, show="*")
Pass.place(x=1030, y=440)

forget = Button(root, text="Forgot Password? ", font=('arial', 16), bg='#8c816f', fg='#ee0000', cursor="hand2",
                command=forgot_password_window, relief=FLAT, activebackground='#8c816f', height=1)
forget.place(x=1030, y=475)

submit = Button(root, text="LOGIN", font=('Times', 13, 'bold'), fg='white', bg='green', activebackground='lightblue',
                width=10, height=2, command=login, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
submit.place(x=1100, y=530)

label2 = Label(root, text="Don't have an account? ", font=('times', 16), fg='black', bg='lightgray', height=1)
label2.place(x=890, y=615)

newlogin = Button(root, text='SIGN UP', font=('Times', 13, 'bold'), fg='white', bg='green', activebackground='lightblue',
                  width=10, height=2, command=newLogin, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
newlogin.place(x=1100, y=600)

root.mainloop()

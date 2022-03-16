from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import datetime
import tkinter.ttk as ttk
import os
import tempfile
#import pkg_resources.py2_warn

import sys
import time

import webbrowser as wb
import fpdf
from fpdf import FPDF

import requests
import base64
from requests.auth import HTTPBasicAuth


# ========================================Function for lipa na mpesa===============================================================================================================================================
# requesting lipa na mpesa from safaricom daraja API.
# The consumer key and secret is for JTTIMBERYARD SAND BOX
def mpay():
    consumer_key = ""  # Consumer Key
    consumer_secret = ""  # Consumer Secret
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    response = r.json()

    access_token = response['access_token']

    phone = PHONE.get()
    saa = datetime.datetime.now()
    timestamp_format = saa.strftime("%Y%m%d%H%M%S")

    businessshortcode = "174379"

    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # pass_key

    pd_decode = businessshortcode + passkey + timestamp_format

    ret = base64.b64encode(pd_decode.encode())

    pd = ret.decode('utf-8')

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": businessshortcode,
        "Password": pd,
        "Timestamp": timestamp_format,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": phone,
        "PartyB": businessshortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://41.139.244.238:80/callback",
        "AccountReference": "28774056",
        "TransactionDesc": "fee payment"
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


# Now we create the lipa na M-pesa window menu

def lipanampesa():
    global payments, PHONE, currentorder, lbl_error, amountpayable
    payments = Tk()
    payments.title("Lipa Na Mpesa")
    width = 700
    height = 600
    screen_width = payments.winfo_screenwidth()
    screen_height = payments.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    payments.resizable(0, 0)
    payments.geometry("%dx%d+%d+%d" % (width, height, x, y))

    currentorder = StringVar()
    PHONE = IntVar()
    TopLoginForm = Frame(payments, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Recieve Payments Via Mpesa", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(payments, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_password = Label(MidLoginForm, text="PHONE NUMBER:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_error = Label(MidLoginForm, text="ENTER PHONE NUMBER TO RECQUEST PAYMENTS e.g :254110919165",
                      font=('arial', 16), bd=18, fg="red")
    lbl_error.grid(row=5, columnspan=2, pady=20)

    PHONE = Entry(MidLoginForm, textvariable=PHONE, font=('arial', 25), width=15)
    PHONE.grid(row=1, column=1)

    btn_login = Button(MidLoginForm, text="SAFARICOM", font=('arial', 18), width=30, bg="green", command=mpay)
    btn_login.grid(row=2, columnspan=2, pady=20)

    btn_login = Button(MidLoginForm, text="Recieve PAYMENTS", font=('arial', 18), width=30, bg="green", command=saveoders)
    btn_login.grid(row=4, columnspan=2, pady=20)

    btn_login = Button(MidLoginForm, text="AIRTEL", font=('arial', 18), width=30, bg="brown", command=mpay)
    btn_login.grid(row=3, columnspan=2, pady=20)
    currentorder.focus


# DECLEARING THE VARIABLES FOR ROOT

root = Tk()
root.title("JT  TIMBER YARD")

width = 1024
height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

# ========================================GLOBAL VARIABLES#===============================================================================================================================================
USERNAME = StringVar()
PASSWORD = StringVar()
USERTYPE = StringVar()
WOODTYPE = StringVar()
WOODSIZE = StringVar()


# ========================================CREATING THE SQLITE-3 DATABASE==================================================================================================================================================
# Not we can change it to mysql database
def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, usertype TEXT, date DATE NOT NULL DEFAULT current_date)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Products` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, wood_type TEXT, wood_size TEXT, total_feet INTEGER, wood_price INTEGER, date DATE NOT NULL DEFAULT current_date)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `employees` (emp_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, IDNO TEXT, FNAME TEXT, POSITION TEXT, PNUM TEXT, date DATE NOT NULL DEFAULT current_date)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Orderz` (order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, OrderNum TEXT, item TEXT, muigana TEXT, quantity INTEGER, thogora INTEGER, total INTEGER, date DATE NOT NULL DEFAULT current_date,waiter TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `ordernumbers` (ordernum_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ordernum TEXT, total INTEGER, amount_paid INTEGER, date DATE NOT NULL DEFAULT current_date)")
    # cursor.execute("DROP TABLE Orderz")

    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password,usertype) VALUES('admin', 'admin', 'Admin')")
        conn.commit()


# ========================================exit#===============================================================================================================================================
def Exit():
    result = tkMessageBox.askquestion('', 'Are you sure you want to exit!', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


# ========================================exit2#===============================================================================================================================================
def Exit2():
    Home.destroy()


# ========================================showloginform#===============================================================================================================================================
def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("JT  TIMBER YARD")
    width = 600
    height = 520
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    loginform.config(bg="darkgreen")
    LoginForm()


# ========================================loginform#===============================================================================================================================================
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="JT TIMBER YARD LOGIN ", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_text = Label(TopLoginForm, text="Enter your user name, password, and user type  ", font=('arial', 18), fg="red",
                     width=600)
    lbl_text.pack(side=TOP, fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_respo = Label(MidLoginForm, text="User Type", font=('arial', 25), bd=18)
    lbl_respo.grid(row=2)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 16), bd=10)
    lbl_result.grid(row=4, columnspan=4)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    USERTYPe = ttk.Combobox(MidLoginForm, textvariable=USERTYPE, font=('arial', 25), width=15, )
    USERTYPe['values'] = ("Admin", "Cashier", "Others")
    USERTYPe.grid(row=2, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=30, command=Login)
    btn_login.grid(row=3, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)
    username.focus()


# ========================================loginform#===============================================================================================================================================
def adduser():
    Database()
    cursor.execute("INSERT INTO `admin` (username, password,usertype) VALUES(?, ?, ?)",
                   (str(Username.get()), str(Password.get()), str(uSERTYPE.get())))
    result = tkMessageBox.showinfo('User account created successfully........!', icon="info")
    conn.commit()
    cursor.close()
    conn.close()
    Username.delete(0, END)
    Password.delete(0, END)
    uSERTYPE.delete(0, END)
    Username.focus()


# ========================================loginform#===============================================================================================================================================

def adduser_form():
    global adminform, lbl_result, Username, Password, uSERTYPE
    adminform = Tk()
    adminform.title("JT  TIMBER YARD USER LOGIN PANEL")
    width = 900
    height = 520
    screen_width = adminform.winfo_screenwidth()
    screen_height = adminform.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    adminform.resizable(0, 0)
    adminform.geometry("%dx%d+%d+%d" % (width, height, x, y))

    Username = StringVar()
    Password = StringVar()
    uSERTYPE = StringVar()
    TopLoginForm = Frame(adminform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Create User Account", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(adminform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_respo = Label(MidLoginForm, text="User Type", font=('arial', 25), bd=18)
    lbl_respo.grid(row=2)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 16), bd=10)
    lbl_result.grid(row=4, columnspan=4)
    Username = Entry(MidLoginForm, textvariable=Username, font=('arial', 25), width=15)
    Username.grid(row=0, column=1)
    Password = Entry(MidLoginForm, textvariable=Password, font=('arial', 25), width=15, show="*")
    Password.grid(row=1, column=1)
    uSERTYPE = ttk.Combobox(MidLoginForm, font=('arial', 25), width=15, )
    uSERTYPE['values'] = ("Admin", "Cashier", "Others")
    uSERTYPE.grid(row=2, column=1)
    btn_login = Button(MidLoginForm, text="Create Account", font=('arial', 18), width=30, command=adduser)
    btn_login.grid(row=3, columnspan=2, pady=20)


# ========================================loginform#===============================================================================================================================================
def recieve_payments():
    global payments, amountpaid, currentorder, lbl_error, amountpayable
    payments = Tk()
    payments.title("JT  TIMBER YARD")
    width = 700
    height = 520
    screen_width = payments.winfo_screenwidth()
    screen_height = payments.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    payments.resizable(0, 0)
    payments.geometry("%dx%d+%d+%d" % (width, height, x, y))
    payments.config(bg="green")

    currentorder = StringVar()
    amountpaid = IntVar()
    TopLoginForm = Frame(payments, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Recieve Payments", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(payments, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Reciept / Invoice No:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="AMOUNT PAID:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_error = Label(MidLoginForm, text="", font=('arial', 25), bd=18)
    lbl_error.grid(row=3, columnspan=2, pady=20)
    Database()
    cursor.execute(
        "select ordernum, total FROM ordernumbers where amount_paid is null ORDER BY ordernum_id DESC limit '1'")
    fetch = cursor.fetchall()
    ids = {}
    for row in fetch:
        ids[row[0]] = [str(FNAME) for FNAME in row[0].split(',')]
        amountpayable = int(row[1])
    currentorder = ttk.Combobox(MidLoginForm, values=list(ids.values()), width=15, textvariable=currentorder,
                                font=('arial', 25))
    currentorder.grid(row=0, column=1)
    amountpaid = Entry(MidLoginForm, textvariable=amountpaid, font=('arial', 25), width=15)
    amountpaid.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Recieve", font=('arial', 18), bg="green", width=30, command=lipa)
    btn_login.grid(row=2, columnspan=2, pady=20)
    currentorder.focus


# ========================================STOCK-UPDATE#===============================================================================================================================================
def update_stock():
    global NEWSTOCK, newqty, WoodType, WOODSIZE
    NEWSTOCK = Tk()
    NEWSTOCK.title("JT  TIMBER YARD STOCK")
    width = 900
    height = 520
    screen_width = NEWSTOCK.winfo_screenwidth()
    screen_height = NEWSTOCK.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    NEWSTOCK.resizable(0, 0)
    NEWSTOCK.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # Defining the variables
    WoodType = StringVar()
    newqty = IntVar()
    WOODSIZE = StringVar()

    TopLoginForm = Frame(NEWSTOCK, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="UPDATE WOOD STOCK", font=('arial',18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(NEWSTOCK, width=600)
    MidLoginForm.pack(side=TOP, pady=50)

    # Defining the labels for the add new stock


    lbl_username = Label(MidLoginForm, text="wood Type:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)

    lbl_username = Label(MidLoginForm, text="wood SIZE:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)

    lbl_password = Label(MidLoginForm, text="NEW FEETS:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)

    #lbl_password = Label(MidLoginForm, text="New FEET:", font=('arial', 25), bd=18)
    #lbl_password.grid(row=2)

    Database()
    cursor.execute("select wood_type FROM Products")
    fetch = cursor.fetchall()
    ids = {}
    for row in fetch:
        ids[row[0]] = [str(FNAME) for FNAME in row[0].split(',')]

    # Now we create the entry fields

    WoodType = ttk.Combobox(MidLoginForm, values=list(ids.values()), width=15, textvariable=WoodType,
                            font=('arial', 25))
    WoodType.grid(row=0, column=1)

    cursor.execute("select wood_size FROM Products")
    fetch = cursor.fetchall()
    ids = {}
    for row in fetch:
        ids[row[0]] = [str(size) for size in row[0].split(',')]

    # Now we create the entry fields

    WOODSIZE = ttk.Combobox(MidLoginForm, values=list(ids.values()), width=15, textvariable=WOODSIZE,
                            font=('arial', 20))
    WOODSIZE.grid(row=1, column=1)

    newqty = Entry(MidLoginForm, textvariable=newqty, font=('arial', 25), width=15)
    newqty.grid(row=2, column=1)

    btn_login = Button(MidLoginForm, text="Update", font=('arial', 18), width=30, command=Reset)
    btn_login.grid(row=3, columnspan=2, pady=20)


def Reset():
    if (int(newqty.get()) > 1):
        Database()
        cursor.execute("select wood_type, wood_size, total_feet FROM `Products` WHERE `wood_type` LIKE ? AND "
                       "`wood_size` LIKE ?",('%' + str(WoodType.get()) + '%','%' + str(WOODSIZE.get()) + '%'))
        fetch = cursor.fetchall()
        for row in fetch:
            calc = (int(row[2])) + int(newqty.get())
        cursor.execute("UPDATE Products SET total_feet = ? WHERE wood_type = ? AND wood_size =?", (calc, WoodType.get(), WOODSIZE.get()))
        result = tkMessageBox.showinfo('stock successfully updated....................!', icon="warning")
        if result == 'yes':
            WoodType.delete(0, END)

            newqty.delete(0, END)

        conn.commit()
        DisplayData()
    else:
        newqty.focus()


# ========================================ADMIN-PAGE#===============================================================================================================================================
def Home():
    global Home
    Home = Tk()
    Home.title("JT  TIMBER YARD")
    width = 1024
    height = 600
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(1, 1)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10, fill=Y)
    BTNS = Frame(Home, bd=1, relief=SOLID)
    BTNS.pack(pady=10, fill=Y)
    VIEW = Frame(Home, bd=1, relief=SOLID)
    VIEW.pack(pady=10, fill=Y)
    lbl_display = Label(Title, text="LIST OF OUR WOOD PRODUCTS", font=('arial', 45))
    lbl_display.pack(fill=Y)
    menubar = Menu(Home)
    filemenu = Menu(menubar, font=('Verdana', 14), tearoff=0)
    filemenu2 = Menu(menubar, font=('Verdana', 14), tearoff=0)
    filemenu3 = Menu(menubar, font=('Verdana', 14), tearoff=0)
    filemenu4 = Menu(menubar, font=('Verdana', 14), tearoff=0)
    filemenu5 = Menu(menubar, font=('Verdana', 14), tearoff=0)
    filemenu6 = Menu(menubar, font=('Verdana', 14), tearoff=0)

    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add User", command=adduser_form)
    filemenu3.add_command(label="Add Employee", command=ShowView)
    filemenu4.add_command(label="Sales", command=printorder)
    filemenu5.add_command(label="In Stock", command=instock)
    filemenu6.add_command(label="Help", command=ShowView)

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Add User", menu=filemenu2)
    menubar.add_cascade(label="Employee", menu=filemenu3)
    menubar.add_cascade(label="Reports", menu=filemenu4)
    menubar.add_cascade(label="Stock", menu=filemenu5)
    menubar.add_cascade(label="Help", menu=filemenu6)
    Home.config(menu=menubar)
    Home.config(bg="#6666ff")

    scrollbary = Scrollbar(VIEW, orient=VERTICAL)
    scrollbarx = Scrollbar(VIEW, orient=HORIZONTAL)
    global tree

    tree = ttk.Treeview(VIEW, columns=("ProductID", "Wood Type", "Wood Size", "Total Feet", "Wood Price"),
                        show="headings", selectmode="extended", yscrollcommand=scrollbary.set,
                        xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    tree.heading('ProductID', text="ProductID", anchor=W)
    tree.heading('Wood Type', text="Wood Type", anchor=W)
    tree.heading('Wood Size', text="Wood Size", anchor=W)
    tree.heading('Total Feet', text="Total Feet", anchor=W)
    tree.heading('Wood Price', text="Wood Price", anchor=W)
    tree.pack(side=TOP)

    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    global SEARCH
    SEARCH = StringVar()
    SEARCH = Entry(BTNS, textvariable=SEARCH, font=('arial', 15), width=35)
    SEARCH.pack(side=LEFT, padx=10, fill=X)
    btn_search = Button(BTNS, text="Search", command=Search)
    btn_search.pack(side=LEFT, padx=10, pady=10, ipadx="50")
    btn_reset = Button(BTNS, text="Update", command=update_stock)
    btn_reset.pack(side=LEFT, padx=10, pady=10, ipadx="50")
    btn_delete = Button(BTNS, text="Delete", command=Delete)
    btn_delete.pack(side=LEFT, padx=10, pady=10, ipadx="50")
    btn_NEWPD = Button(BTNS, text="Add New", command=ShowAddNew)
    btn_NEWPD.pack(side=LEFT, padx=10, pady=10, ipadx="50")

    Database()
    cursor.execute("SELECT * FROM `Products`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


# ===============FUNCTION TO SHOW OUR AVAILABLE WOOD TYPE, WOOD SIZE AND FEET#==========================================
def instock():
    instock = Tk()
    instock.title("JTYARD AVAILABLE STOCK );")
    width = 400
    height = 400
    screen_width = instock.winfo_screenwidth()
    screen_height = instock.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    instock.resizable(0, 0)
    instock.geometry("%dx%d+%d+%d" % (width, height, x, y))

    TopLoginForm = Frame(instock, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Current Stock Quantity", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(instock, width=600)
    MidLoginForm.pack(side=TOP, pady=50, )

    scrollbary = Scrollbar(MidLoginForm, orient=VERTICAL)
    scrollbarx = Scrollbar(MidLoginForm, orient=HORIZONTAL)

    scrollbary = Scrollbar(MidLoginForm, orient=VERTICAL)
    scrollbarx = Scrollbar(MidLoginForm, orient=HORIZONTAL)
    viewcartz = ttk.Treeview(MidLoginForm, columns=("Wood Type", "Wood Size", "Wood price", "FEET Instock"),
                             selectmode="extended",
                             height=12, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=viewcartz.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=viewcartz.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    viewcartz.heading('Wood Type', text="Wood Type", anchor=W)
    viewcartz.heading('Wood Size', text="Wood Size", anchor=W)
    viewcartz.heading('Wood price', text="Wood price", anchor=W)
    viewcartz.heading('FEET Instock', text="FEET Instock", anchor=W)
    viewcartz.column('#0', stretch=YES, minwidth=0, width=10)
    viewcartz.column('#1', stretch=YES, minwidth=0, width=100)
    viewcartz.column('#2', stretch=NO, minwidth=0, width=100)
    viewcartz.column('#3', stretch=NO, minwidth=0, width=100)
    viewcartz.pack(side=TOP, fill=X)

    Database()
    cursor.execute(
        "select wood_type, wood_size,wood_price, total_feet-sum(quantity) as 'sold' from Products, Orderz where "
        "wood_type = item AND wood_size=muigana group by wood_type;")
    fetch = cursor.fetchall()
    for data in fetch:
        viewcartz.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


# ========================================SHOW ADD NEW STOCK#============================================================================================================================================

def ShowAddNew():
    global addnewform
    addnewform = Tk()
    addnewform.title("ADD NEW STOCK")
    width = 600
    height = 500
    screen_width = addnewform.winfo_screenwidth()
    screen_height = addnewform.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()


# ========================================FORM TO ADDD NEW STOCK ============================================================================================================================================
def AddNewForm():
    global WOOD_TYPE, wood_price, WOOD_SIZE, total_feet

    # Top header
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)

    # Now defineing the labels for new stock form

    lbl_text = Label(TopAddNew, text="Add New Products", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=50)

    lbl_productname = Label(MidAddNew, text="Wood Type:", font=('arial', 25), bd=10)
    lbl_productname.grid(row=0, sticky=W)

    lbl_wsize = Label(MidAddNew, text="Wood Size:", font=('arial', 25), bd=10)
    lbl_wsize.grid(row=1, sticky=W)

    lbl_qty = Label(MidAddNew, text="Total Feet:", font=('arial', 25), bd=10)
    lbl_qty.grid(row=2, sticky=W)

    lbl_price = Label(MidAddNew, text="Wood Price:", font=('arial', 25), bd=10)
    lbl_price.grid(row=3, sticky=W)

    # Creating the entry fields

    WOOD_TYPE = ttk.Combobox(MidAddNew, textvariable=WOODTYPE, font=('arial', 25), width=15, )
    WOOD_TYPE['values'] = ('Cyprus', "mahogany", 'bluegum', 'pine', 'eucalyptus', 'teak')
    WOOD_TYPE.grid(row=0, column=1)

    WOOD_SIZE = ttk.Combobox(MidAddNew, textvariable=WOODSIZE, font=('arial', 25), width=15, )
    WOOD_SIZE['values'] = ('2*2', '3*1', '3*2', '3*3', '4*1', '4*2', '6*1', '6*2', '8*1', '8*2', '10*1', '10*2')
    WOOD_SIZE.grid(row=1, column=1)

    total_feet = Entry(MidAddNew, font=('arial', 25), width=15)
    total_feet.grid(row=2, column=1)

    wood_price = Entry(MidAddNew, font=('arial', 25), width=15)
    wood_price.grid(row=3, column=1)

    btn_add = Button(MidAddNew, text="Add", font=('arial', 18), width=30, bg="#009ACD", command=AddNew)
    btn_add.grid(row=4, columnspan=2, pady=20)


# =======================================INSERT-NEW-Products#========================================================================================================================================
def AddNew():
    Database()
    cursor.execute("INSERT INTO `Products` (wood_type, wood_size, total_feet, wood_price) VALUES(?, ?,?, ?)",
                   (str(WOOD_TYPE.get()), str(WOOD_SIZE.get()), int(total_feet.get()), int(wood_price.get())))
    conn.commit()
    WOOD_TYPE.delete(0, END)
    wood_price.delete(0, END)
    total_feet.delete(0, END)
    WOOD_SIZE.delete(0, END)
    cursor.close()
    conn.close()
    DisplayData()
    print("Data added successfully")


# =======================================Function to add  yard employees#========================================================================================================================================
def AddEmp():
    Database()
    cursor.execute("INSERT INTO `employees` (IDNO, FNAME, POSITION, PNUM) VALUES(?, ?, ?, ?)",
                   (str(IDNO.get()), str(FNAME.get()), str(POSITION.get()), str(PNUM.get())))
    conn.commit()
    FNAME.delete(0, END)
    IDNO.delete(0, END)
    POSITION.delete(0, END)
    PNUM.delete(0, END)
    cursor.close()
    conn.close()


# ========================================RORM FOR ADDING EMPLOYEEES JT YARD===========================================
def ViewForm():
    print("employees form called:")
    global tree, FNAME, IDNO, POSITION, PNUM
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=300)
    MidViewForm.pack(side=RIGHT, fill=Y)
    lbl_text = Label(TopViewForm, text="ADD EMPLOYEE", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Full Name", font=('arial', 25))
    lbl_txtsearch.pack(side=TOP, anchor=W, fill=X, pady=10)
    lbl_txtsearch = Label(LeftViewForm, text="ID Number", font=('arial', 25))
    lbl_txtsearch.pack(side=TOP, anchor=W, fill=X, pady=10)
    lbl_txtsearch = Label(LeftViewForm, text="Position", font=('arial', 25))
    lbl_txtsearch.pack(side=TOP, anchor=W, fill=X, pady=10)
    lbl_txtsearch = Label(LeftViewForm, text="Phone Number", font=('arial', 25))
    lbl_txtsearch.pack(side=TOP, anchor=W, fill=X, pady=10)
    FNAME = Entry(MidViewForm, font=('arial', 25))
    FNAME.pack(side=TOP, padx=10, fill=X, pady=10)
    IDNO = Entry(MidViewForm, font=('arial', 25))
    IDNO.pack(side=TOP, padx=10, fill=X, pady=10)
    POSITION = ttk.Combobox(MidViewForm, width=60, font=('arial', 25))
    POSITION['values'] = ("Manager", "Waiter", "Cashier", "Others")
    POSITION.pack(side=TOP, padx=10, fill=X, pady=10)
    PNUM = Entry(MidViewForm, font=('arial', 25))
    PNUM.pack(side=TOP, padx=10, fill=X, pady=10)
    btn_add = Button(MidViewForm, text="Save", font=('arial', 25), bg="#009ACD", command=AddEmp)
    btn_add.pack(side=TOP, padx=10, fill=X, pady=10)
    print("employee added and form closed ")


# ========================================DISPLAYING WOODS#===============================================================================================================================================
def DisplayData():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `Products`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


# ========================================SEARCH-Products#===============================================================================================================================================
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `Products` WHERE `wood_type` LIKE ?", ('%' + str(SEARCH.get()) + '%'))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


# ========================================DELETE-Products#===============================================================================================================================================
def Delete_transaction():
    global Delete_transaction, OnuM, lbl_Error
    Delete_transaction = Tk()
    Delete_transaction.title("JT  TIMBER YARD")
    width = 600
    height = 300
    screen_width = Delete_transaction.winfo_screenwidth()
    screen_height = Delete_transaction.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    Delete_transaction.resizable(0, 0)
    Delete_transaction.geometry("%dx%d+%d+%d" % (width, height, x, y))

    OnuM = StringVar()
    MidLoginForm = Frame(Delete_transaction, width=600)
    MidLoginForm.pack(side=TOP, pady=20)
    lbl_username = Label(MidLoginForm, text="Transaction No:", font=('arial', 20), width=15, bd=18)
    lbl_username.grid(row=0)
    lbl_Error = Label(MidLoginForm, text="", font=('arial', 20), bd=18)
    lbl_Error.grid(row=3, columnspan=2, pady=20)
    Database()
    cursor.execute("select ordernum FROM ordernumbers where total > '0' ORDER BY ordernum_id DESC")
    fetch = cursor.fetchall()
    ids = {}
    for row in fetch:
        ids[row[0]] = [str(FNAME) for FNAME in row[0].split(',')]
    OnuM = ttk.Combobox(MidLoginForm, values=list(ids.values()), width=15, textvariable=OnuM, font=('arial', 20))
    OnuM.grid(row=0, column=1)
    btn_login = Button(MidLoginForm, text="Delete", font=('arial', 20), width=30, command=Erase_transaction)
    btn_login.grid(row=2, columnspan=2, pady=20)
    OnuM.focus


# ========================================DELETE-Products#===============================================================================================================================================

def Erase_transaction():
    if (OnuM.get() == ""):
        lbl_Error.config(text="Select Transaction.....!!", fg="red")
        OnuM.focus
    else:
        result = tkMessageBox.showinfo('Erased Transaction', "Transaction successfully Deleted...!")
        Database()
        cursor.execute("UPDATE ordernumbers  SET total = ? WHERE ordernum=?", (int(0), (OnuM.get())))
        cursor.execute("UPDATE Orderz  SET quantity = ? WHERE ordernum=?", (int(0), (OnuM.get())))
        conn.commit()
        Delete_transaction.destroy()
        vieworders.delete(*vieworders.get_children())
        vieworderz()


# ========================================DELETE-Products#===============================================================================================================================================
def Delete():
    if not tree.selection():
        print("ERROR")
    else:
        result = tkMessageBox.showinfo(title="Delete Record", message="Are you sure you want to delete this record?")
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        tree.delete(curItem)
        Database()
        cursor.execute("DELETE FROM `Orderz` WHERE `product_id` = %d" % selecteditem[0])
        conn.commit()
        cursor.close()
        conn.close()


# ========================================SHOWVIEW#===============================================================================================================================================
def ShowView():
    global viewform
    viewform = Tk()
    viewform.title("JT TIMBER YARD /View Products")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()


# ========================================LOGIN#======================================================================
def Login(event=None):
    global admin_id, Username
    Username = USERNAME.get()
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "" or USERTYPE.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ? AND `usertype` = ?",
                       (USERNAME.get(), PASSWORD.get(), USERTYPE.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ? AND `usertype` = ?",
                           (USERNAME.get(), PASSWORD.get(), USERTYPE.get()))
            data = cursor.fetchone()
            admin_id = data[3]
            usertype = data[3]
            USERNAME.set("")
            PASSWORD.set("")
            USERTYPE.set("")
            lbl_result.config(text="")
            if (usertype == "Admin"):
                ShowHome()
                loginform.destroy()
                root.destroy()

            else:
                Cashier()
                loginform.destroy()
                root.destroy()

        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")


def cashierX():
    cashier.destroy()


def create_ordernum():
    global ordernum
    Database()
    cursor.execute("SELECT count(*) FROM `ordernumbers`")
    fetchdata = cursor.fetchall()
    for r in fetchdata:
        ordernum = int(r[0])


def addtocart():
    if (len(ITEM.get()) == 0 or int(total_feet.get()) < int(1)):
        LBL_ERROR.config(text="NO DATA ENTERED PLEASE ENTER FEET AND WOOD TYPE", fg="red")
        ITEM.delete(0, END)
        total_feet.delete(0, END)
        WOODSIZE.delete(0, END)
        ITEM.focus()
    else:

        create_ordernum()
        global Orders, OrderNum, Sum
        OrderNum = ("RMS00" + str(ordernum + 1))
        Database()
        cursor.execute("SELECT wood_type, wood_size, total_feet, wood_price FROM `Products` WHERE `wood_type` LIKE ?",
                       ('%' + str(ITEM.get()) + '%',))
        rows = cursor.fetchone()
        for row in rows:

            wood_price = int(rows[3])
            pq = int(rows[2])
            cursor.execute("SELECT ifnull(sum(quantity),0) FROM `Orderz` WHERE `item` LIKE ?",
                           ('%' + str(ITEM.get()) + '%',))
            Ret = cursor.fetchone()
            for sold in Ret:
                d = int(sold)
                ev = int(total_feet.get()) + int(sold)
                if pq < ev:
                    Error = pq - d
                    error = str("Insufficient FEETs! Reduce your  feet to:") + str(Error)
                    LBL_ERROR.config(text=error, fg="red")
                    total_feet.delete(0, END)
                    total_feet.focus()
                else:
                    LBL_ERROR.config(text="", fg="red")
                    total = int(total_feet.get()) * wood_price
                    Orders = [(OrderNum, ITEM.get(), WOODSIZE.get(), int(total_feet.get()), wood_price, total, WNAME)]
                    cart.extend(Orders)
                    chekicart()
                    ITEM.delete(0, END)
                    total_feet.delete(0, END)
                    WOODSIZE.delete(0, END)
                    TP.append(total)
                    Sum = sum(TP)
                    showtotal = str("Total Purchases: ") + str(Sum)
                    LBL_TOTAL.config(text=showtotal, fg="brown")


def chekicart():
    viewcartz.delete(*viewcartz.get_children())
    for data in cart:
        viewcartz.insert('', 'end', values=(data))


def vieworderz():
    Database()
    cursor.execute(
        "SELECT OrderNum, item, muigana, quantity, thogora, total FROM `Orderz` where quantity > '0' ORDER BY order_id DESC")
    fetch = cursor.fetchall()
    for data in fetch:
        vieworders.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def reciept_pdf():
    Database()
    cursor.execute(
        "select ordernum, coalesce(sum(total),0) as totalsum FROM Orderz where OrderNum ='%s' group by OrderNum ORDER BY order_id DESC" % (
            OrDerNum))
    fetch = cursor.fetchall()
    pdf = FPDF('p', 'cm', (10, 12))
    pdf.set_font('Arial', 'B', 12)
    pdf.add_page()
    pdf.cell(0, 1, ' JT TIMBER YARD ', 0, ln=1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 1, 'CELL: 0110919165', 0, ln=1)
    pdf.cell(0, 1, 'ADDRESS: P.O Box 45 MATATHIA', 0, ln=1)
    pdf.cell(0, 1, 'www.JTYARD.co.ke', 0, ln=1)
    pdf.cell(2, 1, 'DATE:', 0)
    pdf.cell(6, 1, saa, 0, ln=1)
    pdf.set_font('Arial', 'B', 8)

    for cols in fetch:
        onn = str(cols[0])
        stt = str(cols[1])

    cursor.execute("select OrderNum, item, muigana, quantity, thogora, total FROM `Orderz` WHERE OrderNum='%s'" % (onn))
    vitu = cursor.fetchall()
    pdf.cell(5, 1, 'wood type', 0)
    pdf.cell(5, 1, 'wood size', 0)
    pdf.cell(4, 1, 'QTY', 0)
    pdf.cell(4, 1, 'PRICE', 0)
    pdf.cell(4, 1, 'TOTAL', 0, ln=1)
    for T in vitu:
        pdf.cell(5, 1, str(T[1]), 0)
        pdf.cell(4, 1, str(T[2]), 0)
        pdf.cell(4, 1, str(T[3]), 0)
        pdf.cell(4, 1, str(T[4]), 0, ln=1)
    pdf.cell(4, 1, 'Vat', 0)
    pdf.cell(4, 1, '16%', 0, ln=1)
    pdf.cell(4, 1, 'Total Price', 0)
    pdf.cell(4, 1, stt, 0, ln=1)
    pdf.cell(4, 1, 'Amount Paid', 0)
    pdf.cell(4, 1, str(amountpaid), 0, ln=1)
    pdf.cell(4, 1, 'Balance', 0)
    pdf.cell(4, 1, str(bal), 0, ln=1)
    pdf.cell(4, 1, 'RECIEPT / INVOICE NO:', 0)
    pdf.cell(4, 1, str(OrDerNum), 0, ln=1)
    pdf.cell(0, 1, 'Goods Once Sold can NOT be Returned', 0, ln=1)
    pdf.cell(1, 1, '***THANKYOU FOR BUILDING WITH US @ JT 2022***', 0, ln=1)
    pdf.output('orderreceipt.pdf', 'F')
    wb.open_new(r'orderreceipt.pdf')
    cursor.close()
    conn.close()


def printorder():
    Database()
    cursor.execute(
        "SELECT OrderNum, waiter, item, muigana, quantity, thogora, total, date FROM `Orderz` ORDER BY order_id DESC")
    fetch = cursor.fetchall()
    pdf = FPDF('l', 'mm', 'A4')
    pdf.add_page('l')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Order Number', 1)
    pdf.cell(40, 10, 'Cashier Name', 1)
    pdf.cell(50, 10, 'wood type', 1)
    pdf.cell(50, 10, 'wood size', 0)
    pdf.cell(40, 10, 'Price', 1)
    pdf.cell(30, 10, 'Total feet', 1)
    pdf.cell(40, 10, 'Total amount', 1)
    pdf.cell(40, 10, 'Date', 1, ln=1)
    for y in fetch:
        pdf.cell(40, 10, str(y[0]), 1)
        pdf.cell(40, 10, str(y[1]), 1)
        pdf.cell(50, 10, str(y[2]), 1)
        pdf.cell(50, 10, str(y[3]), 1)
        pdf.cell(40, 10, str(y[4]), 1)
        pdf.cell(30, 10, str(y[5]), 1)
        pdf.cell(40, 10, str(y[6]), 1)
        pdf.cell(40, 10, str(y[7]), 1, ln=1)
    pdf.output('demo.pdf', 'F')
    wb.open_new(r'demo.pdf')
    cursor.close()
    conn.close()


def saveoders():
    if cart == []:
        LBL_TOTAL.config(text="Sorry your Cart is empty pliz add products.....!", fg="red")
        ITEM.focus()

    else:
        Database()
        ITEM.delete(0, END)
        WOODSIZE.delete(0, END)
        Database()
        cursor.execute('insert into ordernumbers (ordernum) values("%s")' % (OrderNum))
        for t in cart:
            cursor.execute(
                "INSERT INTO `Orderz` (OrderNum, item, muigana, quantity, thogora, total, waiter) VALUES(?,?,?,?,?,?,?)",
                t)
            cursor.execute("select ordernum FROM ordernumbers ORDER BY ordernum_id DESC LIMIT 1")
            onum = cursor.fetchone()
            p = str(onum[0])
        cursor.execute(
            "select OrderNum, coalesce(sum(total),0) as totalsum FROM Orderz GROUP BY OrderNum ORDER BY order_id DESC LIMIT 1")
        l = cursor.fetchall()
        for h in l:
            cursor.execute("UPDATE ordernumbers  SET total = ? WHERE ordernum=?", (int(h[1]), p))
        conn.commit()
        create_ordernum()
        LBL_TOTAL.config(text="", fg="brown")

        # Clear the left treeview

        vieworders.delete(*vieworders.get_children())
        vieworderz()
        removefrom_cart()
        recieve_payments()
        tp = str("Total Cost: ") + str(Sum)
        lbl_error.config(text=tp, fg="red")


def lipa():
    global amountpaid, bal, OrDerNum
    amountpaid = int(amountpaid.get())
    OrDerNum = currentorder.get()
    if (amountpaid >= amountpayable):
        bal = amountpaid - amountpayable
        showbal = "Your Balance is: " + str(bal)
        Database()
        cursor.execute("UPDATE ordernumbers SET amount_paid = ? WHERE ordernum = ?", (amountpaid, OrDerNum))
        lbl_error.config(text=showbal, fg="green")
        conn.commit()
        cursor.close()
        conn.close()
        result = tkMessageBox.showinfo('Payment', "Payment successfully recorded...!")
        payments.destroy()
        reciept_pdf()

    else:
        payments.destroy()
        recieve_payments()
        errormsg = str("your total purchase is: ") + str(amountpayable)
        lbl_error.config(text=errormsg, fg="red")
        amountpaid.focus()


def removefrom_cart():
    cart.clear()
    TP.clear()
    chekicart()
    LBL_TOTAL.config(text="", fg="brown")


# ========================================SHOW-home#===============================================================================================================================================
now = datetime.datetime.now()
saa = now.strftime('%d / %m / %Y - %H:%M:%S')


def Cashier():
    global cashier, WNAME, ITEM, cart, total_feet, listbox, LBL_ERROR, LBL_TOTAL, TP, Sum, WOODSIZE
    WNAME = StringVar()
    ITEM = StringVar()
    WOODSIZE = StringVar()
    total_feet = IntVar()
    cart = []
    TP = []
    not_executed = 1
    cashier = Tk()
    cashier.title("JT  TIMBER YARD")

    width = 1024
    height = 520
    screen_width = cashier.winfo_screenwidth()
    screen_height = cashier.winfo_screenheight()
    x = (screen_width) - (width)
    y = (screen_height) - (height)
    cashier.resizable(1, 1)
    screen_width = cashier.winfo_screenwidth()
    x = int(screen_width / 2)

    TopForm = Frame(cashier, bd=5, relief=SOLID, bg="brown")
    TopForm.pack(side=TOP, fill=X)
    lbl_TopForm = Label(TopForm, text="JT  TIMBER YARD CASHIER PANEL", font=('Arial Black', 10), bg="brown",
                        fg="blue")
    lbl_TopForm.pack(fill="both")
    lbl_Time = Label(TopForm, font=('Arial Black', 10), bg="brown", fg="powder blue")
    lbl_Time.pack(fill="both")

    def tick():
        Saa = time.strftime('%A %B  %dTh %Y - %H:%M:%S')
        lbl_Time.config(text=Saa)
        lbl_Time.after(10, tick)

    tick()

    LeftForm = Frame(cashier, bd=3, bg="powder blue", relief=RAISED, width=512, height=100)
    LeftForm.pack(side=LEFT, fill="both")

    LeftFormt = Frame(LeftForm, bd=3, bg="powder blue", relief=RAISED, width=x, height=100)
    LeftFormt.pack(side=TOP, fill='both', expand=False)

    lbl_LeftForm = Label(LeftFormt, text="ENTER WOOD SALE", font=('arial', 10), bg="powder blue")
    lbl_LeftForm.grid(row=0, column=0, pady=10)

    WNAME = Username

    Database()
    LBLWN = Label(LeftFormt, text="WOOD TYPE:", font=('arial', 10), bg="powder blue")
    LBLWN.grid(row=1, column=0, pady=10)
    Database()
    cursor.execute("SELECT wood_type FROM `Products`")
    fetch = cursor.fetchall()
    PDN = {}
    for Rows in fetch:
        PDN[Rows[0]] = [str(wood_type) for wood_type in Rows[0].split(',')]
    ITEM = ttk.Combobox(LeftFormt, values=list(PDN.values()), width=15, font=('arial', 10))
    ITEM.grid(row=1, column=1, pady=10)

    Database()
    cursor.execute("SELECT wood_size FROM `Products`")
    fetch = cursor.fetchall()
    PDN = {}
    for Rows in fetch:
        PDN[Rows[0]] = [str(wood_size) for wood_size in Rows[0].split(',')]
    WOODSIZE = ttk.Combobox(LeftFormt, values=list(PDN.values()), width=15, font=('arial', 10))
    WOODSIZE.grid(row=1, column=4, pady=10)

    LBLONUM = Label(LeftFormt, text="Total feets", font=('arial', 10), bg="powder blue")
    LBLONUM.grid(row=2, column=0, pady=10)

    LBLWOODSIZE = Label(LeftFormt, text=" SELECT Wood Size", font=('arial', 10), bg="powder blue")
    LBLWOODSIZE.grid(row=1, column=3, pady=10)

    total_feet = Entry(LeftFormt, font=('arial', 10), width=15)
    total_feet.grid(row=2, column=1, pady=10)

    LBL_ERROR = Label(LeftFormt, text="", font=('arial', 15), bg="powder blue")
    LBL_ERROR.grid(row=6, column=0, columnspan=20, pady=10)

    btn_s = Button(LeftFormt, text="Empty Cart", width=18, font=('arial', 12), bg="#009ACD", command=removefrom_cart)
    btn_s.grid(row=4, column=0, pady=10)

    btn_s = Button(LeftFormt, text="Add to Cart", width=18, font=('arial', 12), bg="#009ACD", command=addtocart)
    btn_s.grid(row=4, column=1, pady=10)

    # creating the LEFT tree frame

    LeftFormm = Frame(LeftForm, bd=3, width=x, bg="powder blue", relief=RAISED, height=60)
    LeftFormm.pack(side=TOP, fill='both', expand=False)
    # cart view

    scrollbary = Scrollbar(LeftFormm, orient=VERTICAL)
    scrollbarx = Scrollbar(LeftFormm, orient=HORIZONTAL)
    global viewcartz

    scrollbary = Scrollbar(LeftFormm, orient=VERTICAL)
    scrollbarx = Scrollbar(LeftFormm, orient=HORIZONTAL)
    viewcartz = ttk.Treeview(LeftFormm, columns=(
    "Order Number", "Wood Type", "Wood Size", "Total Feet", "Wood Price", "Total price"),
                             selectmode="extended", height=12, yscrollcommand=scrollbary.set,
                             xscrollcommand=scrollbarx.set)
    scrollbary.config(command=viewcartz.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=viewcartz.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    viewcartz.heading('Order Number', text="Order Number", anchor=W)
    viewcartz.heading('Wood Type', text="Wood Type", anchor=W)
    viewcartz.heading('Wood Size', text="Wood Size", anchor=W)
    viewcartz.heading('Total Feet', text="Total Feet", anchor=W)
    viewcartz.heading('Wood Price', text="Wood Price", anchor=W)
    viewcartz.heading('Total price', text="Total price", anchor=W)
    viewcartz.column('#0', stretch=NO, minwidth=0, width=0)
    viewcartz.column('#1', stretch=NO, minwidth=0, width=80)
    viewcartz.column('#2', stretch=NO, minwidth=0, width=120)
    viewcartz.column('#3', stretch=NO, minwidth=0, width=80)
    viewcartz.column('#4', stretch=NO, minwidth=0, width=100)
    viewcartz.column('#5', stretch=NO, minwidth=0, width=120)
    viewcartz.column('#6', stretch=NO, minwidth=0, width=120)

    viewcartz.pack(side=TOP, )

    LBL_TOTAL = Label(LeftFormm, text="", font=('arial', 15), bg="powder blue")
    LBL_TOTAL.pack(side=TOP, )

    btn_sn = Button(LeftFormm, text="Mpesa", width=18, font=('arial', 22), bg="green", command=lipanampesa)
    btn_sn.pack(side=LEFT, )
    btn_sn = Button(LeftFormm, text="Cash", width=18, font=('arial', 22), bg="brown", command=saveoders)
    btn_sn.pack(side=RIGHT, )

    # RIGHT HAND FRAME
    MidForm = Frame(cashier, bd=3, bg="#009ACD", relief=RAISED, height=50)
    MidForm.pack(side=RIGHT, fill='both', expand=False)

    lbl_MidForm = Label(MidForm, width=512, text="LIST OF SALES", font=('arial', 24), bg="#009ACD")
    lbl_MidForm.pack(side=TOP, fill="both")
    scrollbary = Scrollbar(MidForm, orient=VERTICAL)
    scrollbarx = Scrollbar(MidForm, orient=HORIZONTAL)
    global vieworders
    vieworders = ttk.Treeview(MidForm, height=29,
                              columns=("Order Number", "wood type", "total feet", "Price", "Total price"),
                              show="headings", selectmode="extended", yscrollcommand=scrollbary.set,
                              xscrollcommand=scrollbarx.set)
    scrollbary.config(command=vieworders.yview)
    scrollbary.pack(side=RIGHT, fill=Y)

    vieworders.heading('Order Number', text="Order Number", anchor=W)
    vieworders.heading('wood type', text="wood type", anchor=W)
    vieworders.heading('total feet', text="total feet", anchor=W)
    vieworders.heading('Price', text="Price", anchor=W)
    vieworders.heading('Total price', text="Total price", anchor=W)
    vieworders.pack(side=TOP, fill='both', expand=False)

    scrollbarx.config(command=vieworders.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    vieworderz()

    menu = Menu(cashier)
    cashier.config(menu=menu)
    filemenu = Menu(menu, font=('Verdana', 14), tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Exit", command=cashierX)

    lipamenu = Menu(menu, font=('Verdana', 14), tearoff=0)
    menu.add_cascade(label="Payments", menu=lipamenu)
    lipamenu.add_command(label="Recieve Payments", command=recieve_payments)

    helpmenu = Menu(menu, font=('Verdana', 14), tearoff=0)
    menu.add_cascade(label="Reverse", menu=helpmenu)
    helpmenu.add_command(label="Reverse", command=Delete_transaction)

    instockmenu = Menu(menu, font=('Verdana', 14), tearoff=0)
    menu.add_cascade(label="Stock", menu=instockmenu)
    instockmenu.add_command(label="Stock", command=instock)

    reportmenu = Menu(menu, font=('Verdana', 14), tearoff=0)
    menu.add_cascade(label="JT Reports", menu=reportmenu)
    reportmenu.add_command(label="Sales", command=printorder)


# ========================================SHOW-home#===============================================================================================================================================
def ShowHome():
    Home()


# ========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, font=('Verdana', 18), tearoff=0)
filemenu.add_command(label="Login", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# ========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)

# ========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="JT  TIMBER YARD", font=('arial', 50))
lbl_display.pack()
ShowLoginForm()
root.withdraw()

if __name__ == '__main__':
    root.mainloop()

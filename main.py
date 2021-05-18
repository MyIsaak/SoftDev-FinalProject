import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkcalendar import *    
import sqlite3
import random
import requests
from PIL import ImageTk,Image
import json
import os
import matplotlib
from matplotlib.pyplot import Figure
# import emoji  ;)  Because why not !

matplotlib.use('TkAgg')  
root = Tk()
root.geometry("600x400")
root.title('Villasukka')
frame = Frame(root,)

# Login_Labels

sign = Label(frame, text="Login", font=('Arial Bold', 32))
sign.grid(row=0, column=1)

userLabel = Label(frame, text="Username: ")
userLabel.grid(row=1, column=0,)
PasswordLabel = Label(frame, text="Password: ")
PasswordLabel.grid(row=2, column=0, )


# Login_Entrys
userName = Entry(frame, width=35, bd=2)
userName.grid(row=1, column=1, padx=10, pady=10)
Password = Entry(frame, width=35, show='*', bd=2)
Password.grid(row=2, column=1, padx=5, pady=10)

def time():
    # current date and time

    now = datetime.now()
    date_time = now.strftime("%I:%M:%S")
    time_label.config(text=date_time)


def verify_login():
    suffix = []
    user = userName.get()
    passw = Password.get()

    userName.delete(0, END)
    Password.delete(0, END)

    list_of_files = os.listdir()
    for i in list_of_files:
        r_i = i.split('.')
        suffix.append(r_i[0])

    if(user in suffix):
        user_file = open(str(user+".txt"), "r")
        verify = user_file.read().splitlines()
        print(verify)
        if(passw in verify):
            messagebox.showinfo(
                title="Successful", message="Login Successful")
            open_mainwindow()
        else:
            messagebox.showerror(title="Error", message="Wrong Password")
    else:
        messagebox.showerror(title="Error", message="No user found")

def update_Amount():
    conn = sqlite3.connect('Money_Transaction.db')
    c = conn.cursor()
    c.execute("SELECT Balance FROM Account")
    records = c.fetchall()

    totalBalancevar = str(''.join(map(str, records[0])))

    conn.commit()

    amount_label['text'] = "Total amount: "+totalBalancevar+" €"
    amount_label.after(2000, update_Amount)
    conn.close()

def show_frame(frame):
    frame.tkraise()


def show_summary():
    global showWindow
    showWindow = Tk()
    showWindow.geometry("750x500")
    showWindow.title('Villasukka')
    global combodatevar
    global dateCombo

    combodatevar = StringVar()
   
    catLabel = Label(showWindow, text="Month", font=("Arial Bold", 10))
    catLabel.place(x=190, y=40, )

    dateCombo = ttk.Combobox(showWindow, width=30, textvariable=combodatevar)
    dateCombo['values'] = ['January', 'February', 'March', 'April', 'May', 'June', 'August', "September", 'October', 'November', 'December']
    dateCombo.place(x=270, y=40, )
    dateCombo.bind("<<ComboboxSelected>>", __comboBoxCb)

    logoutBtn = Button(showWindow, text="Logout", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    logoutBtn.place(x=580, y=100, )
    returnBtn = Button(showWindow, text="return", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=showWindow.destroy)
    returnBtn.place(x=580, y=150, )

    # summery database
    conn = sqlite3.connect('Money_Transaction.db')
    c = conn.cursor()
    c.execute("select sum(amount) from wallet where TYPE=0")
    records_spend = c.fetchall()
    tot_spend = int(''.join(map(str, records_spend[0])))  # int value

    c.execute("select sum(amount) from wallet where TYPE=1")
    records_in = c.fetchall()
    tot_in = int(''.join(map(str, records_in[0])))  # int value

    conn.commit()
    conn.close()

    tot_saving = (tot_in-tot_spend)

    # some Labels
    spendingLabel = Label(showWindow, text="Spending: " +str(tot_spend), font=("Arial Bold", 10))
    spendingLabel.place(x=580, y=250)
    MoneyinLabel = Label(showWindow, text="Money in: " +str(tot_in), font=("Arial Bold", 10))
    MoneyinLabel.place(x=580, y=200)
    savingLabel = Label(showWindow, text="Money in: " +str(tot_saving), font=("Arial Bold", 10))
    savingLabel.place(x=580, y=300)

def update_savings():

    f = open("savings.txt", 'w')

    open("savings.txt", 'w').close()

    f.write("saving " + str(savingEntry.get()))
    f.write("\n")
    f.write("target " + str(targetLabelEntry.get()))
    f.write("\n")
    f.write("monthly " + str(monthlyEntry.get()))
    messagebox.showinfo(title="Successful", message="Changes Made")
    f.close()

# Lotto

def play_lotto():

    am = 1000
    rnd = random.choice([1, 4, 8, 10, 3, 7, 9, 2])
    print(rnd)
    conn = sqlite3.connect('Money_Transaction.db')
    c = conn.cursor()
    c.execute("SELECT Balance FROM Account")
    records = c.fetchall()
    totbalance = int(''.join(map(str, records[0])))  # int value

    if(rnd % 2 == 0):
        totbalance = totbalance + (am*rnd)
    else:
        totbalance = totbalance - (am*rnd)
    c.execute("""UPDATE Account SET Balance=:balance

                WHERE id = :Id """,
              {
                  'balance': totbalance,
                  'Id': 1
              }
              )

    conn.commit()
    conn.close()
    messagebox.showinfo(title="Lotto", message="Gambling is stupid you have won nothing")



def show_edit():
    global showEditwindow
    showEditwindow = Tk()
    showEditwindow.geometry("980x500")
    showEditwindow.title('Amazing butler App')          #Window configuration (Dimensions, Title, etc...)
    global combodatevar
    global dateCombo

    global daterange_1
    daterange_1 = StringVar()                           #Introducing the date variables as strings
    global daterange_2
    daterange_2 = StringVar()
    combodatevar = StringVar()

    daterangeLabel = Label(showEditwindow, text="Date Range", font=("Arial Bold", 10))             #Label configuration (Dimensions, font, etc...)
    daterangeLabel.place(x=100, y=40, )

    DateEntryRange1 = Entry(showEditwindow, width=35, bd=2, textvariable=daterange_1)               #Configuration for the data entry space
    DateEntryRange1.place(x=250, y=40, )

    DateEntryRange2 = Entry(showEditwindow, width=35,bd=2, textvariable=daterange_2)
    DateEntryRange2.place(x=500, y=40, )

    LogoutButton = Button(showEditwindow, text="Logout", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)    # Logout Btn
    LogoutButton.place(x=820, y=250, )

    ReturnButton = Button(showEditwindow, text="Return", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=showEditwindow.destroy)  # Return Btn
    ReturnButton.place(x=820, y=150, )

    AcceptButton = Button(showEditwindow, text="Accept", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)    # Accept Btn
    AcceptButton.place(x=650, y=200, )
    
    ExportButton = Button(showEditwindow, text="Export to CSV", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=showEditwindow.destroy)
    ExportButton.place(x=820, y=200, )                                                                                                          # Export Btn

    RefreshButton = Button(showEditwindow, text="Refresh", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=showEditwindow.destroy)
    RefreshButton.place(x=650, y=150, )                                                                                                         # Refresh Btn

    # Now going to what we called as a tree
    # total savings = (total income - total expenses)

    TreeFrame = Frame(showEditwindow, width=600, height=280, bg="red")
    TreeFrame.pack(side=LEFT, padx=20)

    # Tree Scroll
    TreeScroll = Scrollbar(TreeFrame)
    TreeScroll.pack(side=RIGHT, fill=Y)

    MyTree = ttk.Treeview(TreeFrame, yscrollcommand=TreeScroll.set, selectmode='extended')
    MyTree.pack()

    TreeScroll.config(command=MyTree.yview)

    MyTree['columns'] = ("ID", "Date", "Amount", "Category")
    MyTree.column("#0", width=0, stretch=NO)
    MyTree.column("ID", anchor=W, width=80)
    MyTree.column("Date", anchor=W, width=120)

    MyTree.column("Amount", anchor=CENTER, width=120)

    MyTree.column("Category", anchor=CENTER, width=120)

def open_mainwindow():
    global clockBtn
    global totalBalancevar
    global amountEntry
    global DateEntry
    global mainWindow
    root.destroy()

    mainWindow = Tk()
    mainWindow.geometry("950x500")
    mainWindow.title('Villasukka App')

    # rootHeight = mainWindow.winfo_height()
    # rootWidth = mainWindow.winfo_width()
    MyOwnMenu = Menu(mainWindow)
    mainWindow.config(menu=MyOwnMenu)

    # MenuItems
    # File
    file_menu = Menu(MyOwnMenu)
    MyOwnMenu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=mainWindow.quit)

    edit_menu = Menu(MyOwnMenu)
    MyOwnMenu.add_cascade(label="Edit", menu=edit_menu)

    option_menu = Menu(MyOwnMenu)
    MyOwnMenu.add_cascade(label="Options", menu=option_menu)

    Tools_menu = Menu(MyOwnMenu)
    MyOwnMenu.add_cascade(label="Tools", menu=Tools_menu)

    Help_menu = Menu(MyOwnMenu)
    MyOwnMenu.add_cascade(label="File", menu=Help_menu)

    # Frames:

    frame_add = Frame(mainWindow, width=280, height=480,)

    frame_add.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    frame_add.grid_propagate(False)

    Frame_1 = Frame(mainWindow, width=590, height=480,)

    Frame_2 = Frame(mainWindow, width=590, height=480,)
    Frame_3 = Frame(mainWindow, width=590, height=480,)

    for frame in (Frame_1, Frame_2, Frame_3):
        frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')
        frame.grid_propagate(False)

    show_frame(Frame_1)

    api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        "Beirut"+"&appid=0ba604883a3d0c62f8151ad357a2f74d"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)

    final_info = condition + " Beirut " + str(temp) + "°C"

    # final info = "NO INTERNET CONNECTION"

    weatherLabel = Label(
        Frame_1, text="weather "+final_info+"", borderwidth=1, relief="solid", font=('Arial Bold', 10))
    weatherLabel.grid(
        row=0, column=0, pady=(0, 20), padx=20, ipadx=10, ipady=10,  sticky='ew')


    global var
    global catvar
    global amountvar
    global datevar
    global totalBalancevar
    totalBalancevar = "N/O"
    var = IntVar()
    datevar = StringVar()
    catvar = StringVar()
    amountvar = StringVar()

    catLabel = Label(Frame_2, text="Category", font=("Arial Bold", 10))
    catLabel.grid(row=0, column=0, pady=(100, 20), padx=(20, 10))
    categoryCombo = ttk.Combobox(Frame_2, width=30, height=10, textvariable=catvar)
    categoryCombo['values'] = ['Rent', 'Travel', 'Groceries', 'Subscription', 'Guilty Pleasures']
    categoryCombo.current(0)
    categoryCombo.grid(row=0, column=1, pady=(100, 20), padx=10, ipadx=5)

    amountLabel = Label(Frame_2, text="Amount", font=("Arial Bold", 10))
    amountLabel.grid(row=1, column=0, pady=(0, 20), padx=(20, 10))

    amountEntry = Entry(Frame_2, width=35, bd=2, textvariable=amountvar)
    amountEntry.grid(row=1, column=1, pady=(0, 20), padx=10)

    dateLabel = Label(Frame_2, text="Date", font=("Arial Bold", 10))
    dateLabel.grid(row=2, column=0, pady=(0, 20), padx=(20, 10))

    dateEntry = Entry(Frame_2, width=35, bd=2, textvariable=datevar)
    dateEntry.insert(0, "Enter manual date or use picker")
    dateEntry.grid(row=2, column=1, pady=(0, 20), padx=10)

    moneyLabel = Label(Frame_2, text="Money in?", font=("Arial Bold", 10))
    moneyLabel.grid(row=3, column=0, pady=(0, 20), padx=(20, 10))

    moneyBox = Checkbutton(Frame_2, variable=var, fg="Blue",)
    moneyBox.grid(row=3, column=1, pady=(0, 20), padx=5, sticky='w')

# Buttons
    LogoutButton = Button(Frame_1, text="Logout", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton.grid(row=0, column=2, pady=20, padx=120)

    TransactionButton = Button(Frame_1, text="Add Transaction", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(Frame_2))
    TransactionButton.grid(row=1, column=2, pady=20, padx=120)

    EditButton = Button(Frame_1, text="Edit account", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=show_edit)
    EditButton.grid(row=2, column=2, pady=20, padx=120)

    SetupButton = Button(Frame_1, text="Setup", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(Frame_3))
    SetupButton.grid(row=3, column=2, pady=20, padx=120)

    SummaryButton = Button(Frame_1, text="Account Summary", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=show_summary)
    SummaryButton.grid(row=4, column=2, pady=20, padx=120)
    PlayButton = Button(Frame_1, text="Play Lotto", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=play_lotto)
    PlayButton.grid(row=5, column=2, pady=20, padx=120)

    ClockButton = PhotoImage(file='images/clockv2.png')

    GetTimeButton = Button(frame_add, image=ClockButton, border=0, command=time)

    GetTimeButton.grid(row=0, column=0, pady=20, padx=5, sticky="ew")


    LogoutButton2 = Button(Frame_2, text="Logout", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton2.grid(row=0, column=3, pady=(100, 20), padx=100)

    TransactionButton2 = Button(Frame_2, text="Add Transaction", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=submit)
    TransactionButton2.grid(row=1, column=3, pady=(0, 20), padx=100)

    CancelButton = Button(Frame_2, text="Cancel and return", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(Frame_1))
    CancelButton.grid(row=2, column=3, pady=(0, 20), padx=100)


    LogoutButton3 = Button(Frame_3, text="Logout", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton3.grid(row=0, column=3, pady=(100, 20), padx=50)

    AcceptButton = Button(Frame_3, text="Accept Changes", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=update_savings)
    AcceptButton.grid(row=1, column=3, pady=(0, 20), padx=50)

    ReturnButton = Button(Frame_3, text="Return", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(Frame_1))
    ReturnButton.grid(row=2, column=3, pady=(0, 20), padx=50)


################################### database

# Time Label
    
    global time_label
    time_label = Label(frame_add, text="Pick Time", font=("Arial", 10))
    time_label.grid(row=1, column=0, pady=5, padx=20,)

    global amount_label
    amount_label = Label(Frame_1, borderwidth=1, relief="solid", font=('Arial Bold', 10))
    amount_label.grid(row=1, column=0, pady=(0, 20), padx=20, ipadx=10, ipady=10,  sticky='ew')

    # Calender

    cal = Calendar(frame_add, selectmode="day", year=2021, month=4, day=27, background="Blue", textvariable=datevar)
    cal.grid(row=2, column=0, pady=20, padx=20, )
    update_Amount()
    conn.close()



conn = sqlite3.connect('Money_Transaction.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS wallet(
       ID INTEGER PRIMARY KEY AUTOINCREMENT,
   DATE           TEXT,
   AMOUNT         INT,
   CATEGORY       TEXT,
   TYPE           INT

    )"""

          )

c.execute("""CREATE TABLE IF NOT EXISTS Account(
            id int UNIQUE,
            Balance INTEGER  )"""

          )

c.execute("Insert or IGNORE INTO Account VALUES(:id,:balance)",

          {'id': 1,
           'balance': 100000
           }


          )
conn.commit()



#LogButtons
loginBtn = Button(frame, text="login", bg="Green",fg="white", height=1, width=10, font="Raleway", command=open_mainwindow)
loginBtn.grid(row=3, column=1, pady=5)


frame.place(relx=0.5, rely=0.5, anchor=CENTER)







conn.close()
root.mainloop()
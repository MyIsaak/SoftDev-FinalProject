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
#import emoji

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
    # print(int(''.join(map(str, records[0]))))  # int value

    totalBalancevar = str(''.join(map(str, records[0])))

    conn.commit()

    amount_label['text'] = "Total amount: "+totalBalancevar+" €"
    amount_label.after(2000, update_Amount)
    conn.close()

def show_frame(frame):
    frame.tkraise()


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

    frame_middle_1 = Frame(mainWindow, width=590, height=480,)

    frame_middle_2 = Frame(mainWindow, width=590, height=480,)
    frame_middle_3 = Frame(mainWindow, width=590, height=480,)

    for frame in (frame_middle_1, frame_middle_2, frame_middle_3):
        frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')
        frame.grid_propagate(False)

    show_frame(frame_middle_1)

    api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        "Beirut"+"&appid=0ba604883a3d0c62f8151ad357a2f74d"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)

    final_info = condition + " Beirut " + str(temp) + "°C"

    # final_info = "NO INTERNET CONNECTION"

    weatherLabel = Label(
        frame_middle_1, text="weather "+final_info+"", borderwidth=1, relief="solid", font=('Arial Bold', 10))
    weatherLabel.grid(
        row=0, column=0, pady=(0, 20), padx=20, ipadx=10, ipady=10,  sticky='ew')

# Buttons
    LogoutButton = Button(frame_middle_1, text="Logout", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton.grid(row=0, column=2, pady=20, padx=120)

    TransactionButton = Button(frame_middle_1, text="Add Transaction", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(frame_middle_2))
    TransactionButton.grid(row=1, column=2, pady=20, padx=120)

    EditButton = Button(frame_middle_1, text="Edit account", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=show_edit)
    EditButton.grid(row=2, column=2, pady=20, padx=120)

    SetupButton = Button(frame_middle_1, text="Setup", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(frame_middle_3))
    SetupButton.grid(row=3, column=2, pady=20, padx=120)

    SummaryButton = Button(frame_middle_1, text="Account Summary", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=show_summary)
    SummaryButton.grid(row=4, column=2, pady=20, padx=120)
    PlayButton = Button(frame_middle_1, text="Play Lotto", bg="Blue", fg="white", height=1, width=15, font="Raleway", command=play_lotto)
    PlayButton.grid(row=5, column=2, pady=20, padx=120)

    ClockButton = PhotoImage(file='images/clockv2.png')

    GetTimeButton = Button(frame_add, image=ClockButton, border=0, command=time)

    GetTimeButton.grid(row=0, column=0, pady=20, padx=5, sticky="ew")


    LogoutButton2 = Button(frame_middle_2, text="Logout", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton2.grid(row=0, column=3, pady=(100, 20), padx=100)

    TransactionButton2 = Button(frame_middle_2, text="Add Transaction", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=submit)
    TransactionButton2.grid(row=1, column=3, pady=(0, 20), padx=100)

    CancelButton = Button(frame_middle_2, text="Cancel and return", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(frame_middle_1))
    CancelButton.grid(row=2, column=3, pady=(0, 20), padx=100)


    LogoutButton3 = Button(frame_middle_3, text="Logout", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=mainWindow.quit)
    LogoutButton3.grid(row=0, column=3, pady=(100, 20), padx=50)

    AcceptButton = Button(frame_middle_3, text="Accept Changes", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=update_savings)
    AcceptButton.grid(row=1, column=3, pady=(0, 20), padx=50)

    ReturnButton = Button(frame_middle_3, text="Return", bg="#4465f9",fg="white", height=1, width=15, font="Raleway", command=lambda: show_frame(frame_middle_1))
    ReturnButton.grid(row=2, column=3, pady=(0, 20), padx=50)


################################### database

# Time Label
    
    global time_label
    time_label = Label(frame_add, text="Pick Time", font=("Arial", 10))
    time_label.grid(row=1, column=0, pady=5, padx=20,)

    global amount_label
    amount_label = Label(frame_middle_1, borderwidth=1, relief="solid", font=('Arial Bold', 10))
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



    # Buttons
loginBtn = Button(frame, text="login", bg="Green",fg="white", height=1, width=10, font="Raleway", command=open_mainwindow)
loginBtn.grid(row=3, column=1, pady=5)


frame.place(relx=0.5, rely=0.5, anchor=CENTER)


conn.close()
root.mainloop()
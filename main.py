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



# functions


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


    # Buttons
loginBtn = Button(frame, text="login", bg="Blue",
                  fg="white", height=1, width=10, font="Raleway", command=open_mainwindow)
loginBtn.grid(row=3, column=1, pady=5)


frame.place(relx=0.5, rely=0.5, anchor=CENTER)



root.mainloop()
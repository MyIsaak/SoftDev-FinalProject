import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import *  # installed
import sqlite3
import random
import requests
import json
import pandas as pd
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use('TkAgg') 

root = Tk()
root.geometry("600x400")
root.title('Villasukka')

frame = Frame(root,)

# Login Tab
sign = Label(frame, text="Login", font=('Arial Bold', 16))
sign.grid(row=0, column=1, pady=(0, 20))

userLabel = Label(frame, text="Username: ")
userLabel.grid(row=1, column=0,)
PasswordLabel = Label(frame, text="Password: ")
PasswordLabel.grid(row=2, column=0, )

# Username & Password
userName = Entry(frame, width=35, bd=2)
userName.grid(row=1, column=1, padx=10, pady=10)
Password = Entry(frame, width=35, show='*', bd=2)
Password.grid(row=2, column=1, padx=5, pady=10)

loginBtn = Button(frame, text="login", bg="Blue", fg="white", height=1, width=10, font="Raleway", command=open_mainwindow)
loginBtn.grid(row=3, column=1, pady=5)

root.mainloop()
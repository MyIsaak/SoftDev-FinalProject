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


# functions


root.mainloop()
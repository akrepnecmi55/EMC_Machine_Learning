import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path



isDbExist = False
isDbTended = False
# p = Path(__file__).parents[2]
# path = os.path.join(p, 'mem\mbDb')
path = 'mbDb'
try:
    with shelve.open(path, writeback=True) as mbDb:
        if ('inc' not in mbDb):
            isDbExist = False
except:
    print("boyle bi db yok")
    


mbDbTk = tk.Tk()
mbDbTk.title("mainboard database configuration")
mbDbTkF = tk.Frame(mbDbTk)
mbDbTkF.grid()

tk.Button(mbDbTkF, text="show top 10", command = lambda: showTop10()).grid(row = 1, column = 1)
print("niye çalışmadı amk")

mainloop()

def showTop10():
    ctr = 0
    for col in mbDb:
        ctr += 1
        tk.Label(mbDbTkF, text=col).grid(row = 2, column = 2+ctr)
        for i in range(10):
            tk.Label(mbDbTkF, text=mbDb[col][i]).grid(row = 2+i, column = 2+ctr)
    tk.Label(mbDbTkF, text="TOP 10").grid(row=1,column=2,columnspan = ctr)
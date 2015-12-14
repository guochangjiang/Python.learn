from tkinter import *
from tkinter.ttk import Combobox

def cbox_do(event):
    'Used for cbox.'
    clabel.config(text=cbox.get())

a = Tk()
cbox = Combobox(a, value=('Luke','Biggs','Wedge'), takefocus=0)
cbox.bind("<<ComboboxSelected>>", cbox_do)
cbox.pack()
clabel = Label(a)
clabel.pack()
a.mainloop()

master = Tk()
variable = StringVar(master)
variable.set("one")
w = Combobox(master, textvariable=variable, values=["one", "two", "three"])
w.pack()

master.mainloop()
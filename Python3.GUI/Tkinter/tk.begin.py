#!/usr/bin/env python3
# --*-- utf-8 --*--

import tkinter as tk #引用tkinter模块

##--Label
root = tk.Tk() #初始化Tk()
root.title("example1: Label") #设置窗口标题
root.geometry('400x200') #设置窗口大小，是x，不是*
root.resizable(width=False, height=True) #宽不可变，高可变，默认为True
left = tk.Label(root, text="左边", bg='green', fg='red', font=("Arial", 12), width=5, height=2)
left.pack(side='left') #side可以赋值为left, right, top, bottom
right = tk.Label(root, text="right", bg='green', fg='red', font=("Arial", 12), width=5, height=2)
right.pack(side='right') #side可以赋值为left, right, top, bottom
top = tk.Label(root, text="top", bg='green', fg='red', font=("Arial", 12), width=5, height=2)
top.pack(side='top') #side可以赋值为left, right, top, bottom
bottom = tk.Label(root, text="bottom", bg='green', fg='red', font=("Arial", 12), width=5, height=2)
bottom.pack(side='bottom') #side可以赋值为left, right, top, bottom
root.mainloop() #进入消息循环


##--Frame
example2 = tk.Tk()
example2.title("example2: Frame")
example2.geometry("300x200")
tk.Label(example2, text="校训", font=("Arial", 20)).pack()

frm = tk.Frame(example2)
#left
frm_L = tk.Frame(frm)
tk.Label(frm_L, text="诚朴", font=("Arial",15)).pack(side="top")
tk.Label(frm_L, text="雄伟", font=("Arial",15)).pack(side="top")
frm_L.pack(side="left")

#right
frm_R = tk.Frame(frm)
tk.Label(frm_R, text="励学", font=("Arial",15)).pack(side="top")
tk.Label(frm_R, text="敦行", font=("Arial",15)).pack(side="top")
frm_R.pack(side="right")
frm.pack()
example2.mainloop()

##--Entry
example3 = tk.Tk()
example3.title("example3: Entry")
example3.geometry("300x200")
var = tk.StringVar()
e = tk.Entry(example3, textvariable = var)
var.set("Hello world")
e.pack()
example3.mainloop()


##--Text
example4 = tk.Tk()
example4.title("example4: Text")
example4.geometry("300x200")
t = tk.Text(example4)
t.insert(1.0, 'hello\n')
t.insert(2.0, "world!\n")
t.insert('2.end', "\n012345")
t.insert('end', 'hello00000\n')
t.insert(2.6, 'nono')
t.pack()
example4.mainloop()

##--Button
example5 = tk.Tk()
example5.title("Example5: Button")
example5.geometry()
def printhello():
    t2.insert('1.0', "hello world\n")

t2 = tk.Text();
t2.pack()
tk.Button(example5, text="press", command=printhello).pack()
example5.mainloop()

##--Listbox
example6 = tk.Tk()
example6.title("example6: Listbox")
example6.geometry()

def print_item(event):
    print(lb.get(lb.curselection()))

var = tk.StringVar()
lb = tk.Listbox(example6, listvariable = var)
list_item = [1, 2, 3, 4]
for item in list_item:
    lb.insert('end', item)
lb.delete(2, 4)
var.set(('a', 'ab', 'c', 'd'))
print(var.get())
lb.bind('<ButtonRelease-1>', print_item)
lb.pack()
example6.mainloop()

##--Scrollbar
example7 = tk.Tk()
example7.title("example7: Scrollbar")
example7.geometry()
var = tk.StringVar()
lb2 = tk.Listbox(example7, height = 5, selectmode="browse", listvariable = var)
lb2.bind('<ButtonRelease-1>', print_item)
list_item = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
for item in list_item:
    lb2.insert('end', item)
scrl = tk.Scrollbar(example7)
scrl.pack(side="right", fill='y')
lb2.configure(yscrollcommand = scrl.set)
lb2.pack(side="left", fill='both')
scrl['command'] = lb2.yview
example7.mainloop()


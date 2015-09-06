#!/usr/bin/env python3
# --*-- utf-8 --*--

import tkinter as tk

def main():
    global root, history_frame, info_line
    root = tk.Tk()
    root.title('Txt2Html TK Shell')
    #init_vars()
    #-- 创建菜单框架
    menu_frame = tk.Frame(root)
    menu_frame.pack(fill = tk.X, side = tk.TOP)
    menu_frame.tk_menuBar(fill_menu(), action_menu(), help_menu())
    #-- 创建历史框架
    history_frame = tk.Frame(root)
    history_frame.pack(fill = tk.X, side = tk.BOTTOM, pady = 2)
    #-- 创建信息框架并添加初始内容
    info_frame = tk.Frame(root)
    info_frame.pack(fill = tk.X, side = tk.BOTTOM)
    #先将栏目标签添加到二级框架
    LEFT, Label = tk.LEFT, tk.Label #快捷方式名称
    label_line = tk.Frame(info_frame, relief=tk.RAISED, borderwidth=1)
    label_line.pack(side=tk.TOP, padx=2, pady=1)
    Label(label_line, text="Run #", width=5).pack(side=LEFT)
    Label(label_line, text="Source:", width=20).pack(side=LEFT)
    Label(label_line, text="Target:", width=20).pack(side=LEFT)
    Label(label_line, text="Type:", width=20).pack(side=LEFT)
    Label(label_line, text="Proxy Mode:", width=20).pack(side=LEFT)
    #再把"下次运行"信息放入二级框架
    info_line = tk.Frame(info_frame)
    info_line.pack(side=tk.TOP, padx=2, pady=1)
    update_specs()
    #-- 最后运行上述定义
    root.mainloop()

#-- 创建下拉菜单
def help_menu():
    help_btn = tk.Menubutton(menu_frame, text = 'Help', underline=0)
    help_btn.pack(side=tk.LEFT, padx="2m")
    help_btn.menu = tk.Menu(help_btn)
    help_btn.menu.add_command(label="How To", underline=0, command=HowTo)
    help_btn.menu.add_command(label="About", underline=0, command=About)
    help_btn['menu'] = help_btn.menu
    return help_btn

#-- 获得用户输入
def GetSource():
    get_window = tk.Toplevel(root)
    get_window.title('Source File?')
    source = tk.StringVar()
    source.set('txt2html.txt')
    source_string = source.get()
    tk.Entry(get_window, width=30, textvariable=source).pack()
    tk.Button(get_window, text = "Change", command = lambda: update_specs()).pack()

main()

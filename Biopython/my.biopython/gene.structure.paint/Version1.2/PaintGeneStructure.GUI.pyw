#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: PaintGeneStructure.GUI.py
#
#        USAGE: usage
#
#  DESCRIPTION: 程序PaintGeneStructure.py的界面化操作程序
#
#      OPTIONS: ---
# REQUIREMENTS:
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/11/16 11:59:42
#       UPDATE: 2015/11/16 11:59:43
#===============================================================================
#   Change logs:
#   Version

__version__ = '1.0'

import tkinter as tk
from tkinter.ttk import Combobox
import os
import re
import subprocess

def StartPainting():
    infile = filevariable.get()
    infileformat = fileformat.get()
    outfile = OutEn.get()
    color = colorEn.get()
    kblength = kbEn.get()
    introntype = intronvar.get()

    if not os.path.exists(infile):
        warninfo = tk.Label(PGS, text = "请输入正确的文件名", fg = "red",
                            bitmap = 'error', compound = 'left')
        warninfo.grid(row = 6, column = 0, columnspan = 4, sticky = "W", padx = 10)
    else:
        options = "-i " + infile + " -o " + outfile + " -kl " + kblength
        options += " -intronline " + introntype + " -format " + infileformat
        if color != "":
            options += " -C " + color
        subprocess.call("pythonw PaintGeneStructure.v1.2.py " + options, shell = False)
        warninfo = tk.Label(PGS, text = "恭喜，绘制完成。输出文件为：" + outfile, fg = "red")
        warninfo.grid(row = 6, column = 0, columnspan = 4, sticky = "W", padx = 10)


PGS = tk.Tk()
PGS.title("基因结构svg图像绘制程序")  #设置窗口标题
PGS.geometry('600x180')              #设置窗口大小

#输入文件信息
filenamelist=os.listdir(os.getcwd())
gfflist = [];
for file in filenamelist:
    if re.search("gff$", file):
        gfflist.append(file)
    
filevariable = tk.StringVar(PGS)
filevariable.set(gfflist[0])
Combobox(PGS, textvariable=filevariable, values=gfflist, width = 20
         ).grid(row = 0, column = 1, sticky = "WE")
infileLabel = tk.Label(PGS, text = "基因信息文件:")
infileLabel.grid(row = 0, column = 0, sticky = "W", padx = 10)
#InEn = tk.StringVar()
#infileEntry = tk.Entry(PGS, textvariable = InEn)
#InEn.set('请输入基因信息文件名')
#infileEntry.grid(row = 0, column = 1, sticky = "E")
tk.Label(PGS, text = "[必需] 文件格式:").grid(row = 0, column = 2, sticky = "W")
fileformat = tk.StringVar()
fileformat.set("auto")
fauto = tk.Radiobutton(PGS, variable = fileformat, text = "auto", value = "auto")
fauto.grid(row = 0, column = 3)
fsimple = tk.Radiobutton(PGS, variable = fileformat, text = "simple", value = "simple")
fsimple.grid(row = 0, column = 4)
fgff = tk.Radiobutton(PGS, variable = fileformat, text = "gff", value = "gff")
fgff.grid(row = 0, column = 5)

#输出文件信息
outfileLabel = tk.Label(PGS, text = "输出文件名:")
outfileLabel.grid(row = 1, column = 0, sticky = "W", padx = 10)
OutEn = tk.StringVar()
OutEn.set("output.svg")
outfileEntry = tk.Entry(PGS, textvariable = OutEn, width = 20)
outfileEntry.grid(row = 1, column = 1, sticky = "WE")
tk.Label(PGS, text = "默认: output.svg").grid(row = 1, column = 2, sticky = "W")

#内含子线型
intronLabel = tk.Label(PGS, text = "内含子线型:")
intronLabel.grid(row = 2, column = 0, sticky = "W", padx = 10)
intronvar = tk.StringVar()
intronvar.set("straight")
intronstraight = tk.Radiobutton(PGS, variable = intronvar, text = "直线", value = "straight")
intronstraight.grid(row = 2, column = 1, sticky = "W")
intronbroken = tk.Radiobutton(PGS, variable = intronvar, text = "折线", value = "broken")
intronbroken.grid(row = 2, column = 1, sticky = "E")

#长度指定
kblenLabel = tk.Label(PGS, text = "每kb图像长度(px):", padx = 10)
kblenLabel.grid(row = 3, column = 0, sticky = "W")
kbEn = tk.StringVar()
kbEn.set("250")
kbEntry = tk.Entry(PGS, textvariable = kbEn, width = 20)
kbEntry.grid(row = 3, column = 1, sticky = "WE")
tk.Label(PGS, text = "默认: 250px/kb").grid(row = 3, column = 2, sticky = "W")

#颜色指定
colorLabel = tk.Label(PGS, text = "颜色指定:", padx = 10)
colorLabel.grid(row = 4, column = 0, sticky = "W")
colorEn = tk.StringVar()
colorEntry = tk.Entry(PGS, textvariable = colorEn, width = 20)
colorEntry.grid(row = 4, column = 1, sticky = "WE")
tk.Label(PGS, text = "默认: 内置方案。"
         ).grid(row = 4, column = 2, sticky = "W")
tk.Label(PGS, text = "定义方法如: CDS:green;LRR:yellow;..."
         ).grid(row = 4, column = 3, columnspan = 4, sticky = "W")

#运行程序
runbutton = tk.Button(PGS, text = "开始绘制", command = StartPainting, padx = 10)
runbutton.grid(row = 5, column = 0, sticky = "W")

PGS.mainloop()


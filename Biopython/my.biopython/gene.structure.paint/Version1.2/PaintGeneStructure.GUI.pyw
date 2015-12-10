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
# REQUIREMENTS: 依赖于程序PaintGeneStructure.v1.2.py
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
from tkinter.filedialog import askopenfilename
import os
import re
import subprocess
gfflist1 = []
fname = ''

def LoadFile():
    fname = askopenfilename(filetypes=(("gff/simple files", "*.gff;*.simple"),
                                           ("All files", "*.*") ))
    if fname:
        selectEn.set(fname)
        selectEntry = tk.Entry(PGS, textvariable = selectEn, width = 50)
        selectEntry.grid(row = 0, column = 1, sticky = "WE", columnspan = 5)
        tk.Button(PGS, text = "选择文件", command = LoadFile
          ).grid(row = 0, column = 6,  sticky = "W")
        gfflist1.append(fname)
        filevariable1.set(fname)
        Combobox(PGS, textvariable=filevariable1, values=gfflist1, width = 50
         ).grid(row = 1, column = 1, sticky = "WE", columnspan = 5)
        #outfileEntry = tk.Entry(PGS, textvariable = OutEn, width = 50)
        #outfileEntry.grid(row = 2, column = 1, sticky = "WE", columnspan = 5)


def StartPainting():
    infile = filevariable1.get()
    fmatch = re.search("([a-zA-Z0-9\.\-_]+)$", infile)
    filename = fmatch.group(1)
    tk.Label(PGS, text = "源文件:" + filename, fg = "blue").grid(row = 8, column = 6, columnspan = 10, sticky = "W")
    outfilename = filevariable1.get()
    outfilename = os.path.basename(outfilename) + ".svg"
    infileformat = fileformat.get()
    outfile = OutEn.get()
    if outfile == '':
        outfile = outfilename
    color = colorEn.get()
    kblength = kbEn.get()
    intronref = intronrefvar.get()
    introntype = intronvar.get()
    if not os.path.exists(infile):
        warninfo = tk.Label(PGS, text = "请输入正确的文件名", fg = "red",
                            bitmap = 'error', compound = 'left')
        warninfo.grid(row = 8, column = 1, columnspan = 4, sticky = "WE", padx = 10)
    else:
        options = "-i " + infile + " -o " + outfile + " -kl " + kblength + " --intronref " + intronref
        options += " -intronline " + introntype + " -format " + infileformat
        if color != "":
            options += " -C " + color
        if os.path.exists(outfile):
            os.remove(outfile)
        subprocess.call("pythonw PaintGeneStructure.v1.2.py " + options
                      + " 1>PaintGeneStructure.log 2>&1", shell = True)
        if os.path.exists(outfile):
            warninfo = tk.Label(PGS, text = "恭喜，绘制完成。输出文件为：程序文件夹/" + outfile, fg = "red")
            warninfo.grid(row = 9, column = 1, columnspan = 5, sticky = "WE", padx = 10)
        else:
            warninfo = tk.Label(PGS, text = "抱歉！程序运行失败，请查看程序目录下的PaintGeneStructure.log", fg = "red")
            warninfo.grid(row = 9, column = 1, columnspan = 5, sticky = "WE", padx = 10)

PGS = tk.Tk()
PGS.title("基因结构svg图像绘制程序")  #设置窗口标题
#PGS.geometry('820x250')              #设置窗口大小
rowflag = 0

#输入文件信息
selectLabel = tk.Label(PGS, text = "基因信息文件:")
selectLabel.grid(row = 0, column = 0, sticky = "E", padx = 10)
selectEn = tk.StringVar()
selectEn.set("")
selectEntry = tk.Entry(PGS, textvariable = selectEn, width = 50)
selectEntry.grid(row = 0, column = 1, sticky = "WE", columnspan = 5)
tk.Button(PGS, text = "选择文件", command = LoadFile
          ).grid(row = 0, column = 6,  sticky = "W")

filenamelist1=os.listdir(os.getcwd())
for file in filenamelist1:
    if re.search("(\.gff$)|(\.simple$)", file):
        gfflist1.append(file)
filevariable1 = tk.StringVar(PGS)
filevariable1.set(gfflist1[0])
Combobox(PGS, textvariable=filevariable1, values=gfflist1, width = 50
         ).grid(row = 1, column = 2, sticky = "WE", columnspan = 4)
rowflag += 1

infileLabel = tk.Label(PGS, text = "或者:")
infileLabel.grid(row = rowflag, column = 1, sticky = "E")
tk.Label(PGS, text = "[必需] 文件格式:").grid(row = rowflag, column = 6, sticky = "W")
fileformat = tk.StringVar()
fileformat.set("auto")
fauto = tk.Radiobutton(PGS, variable = fileformat, text = "auto", value = "auto")
fauto.grid(row = rowflag, column = 7)
fsimple = tk.Radiobutton(PGS, variable = fileformat, text = "simple", value = "simple")
fsimple.grid(row = rowflag, column = 8)
fgff = tk.Radiobutton(PGS, variable = fileformat, text = "gff", value = "gff")
fgff.grid(row = rowflag, column = 9)
rowflag += 1

#输出文件信息
outfilename = ''
inputfname = filevariable1.get()
if '/' in inputfname:
    indir = os.path.dirname(inputfname)
    inname = os.path.basename(inputfname)
    outfilename = indir + inname + ".svg"
else:
    outfilename = inputfname + ".svg"
outfileLabel = tk.Label(PGS, text = "输出文件名:")
outfileLabel.grid(row = rowflag, column = 0, sticky = "E", padx = 10)
OutEn = tk.StringVar()
OutEn.set("")
outfileEntry = tk.Entry(PGS, textvariable = OutEn, width = 50)
outfileEntry.grid(row = rowflag, column = 1, sticky = "WE", columnspan = 5)
tk.Label(PGS, text = "默认: 输入文件名.svg"
         ).grid(row = rowflag, column = 6, sticky = "W", columnspan = 2)
rowflag += 1

#内含子参照
intronLabel = tk.Label(PGS, text = "内含子参照:")
intronLabel.grid(row = rowflag, column = 0, sticky = "E", padx = 10)
intronrefvar = tk.StringVar()
intronrefvar.set("exon")
intronexon = tk.Radiobutton(PGS, variable = intronrefvar, text = "外显子", value = "exon")
intronexon.grid(row = rowflag, column = 1, sticky = "W")
introncds = tk.Radiobutton(PGS, variable = intronrefvar, text = "CDS", value = "CDS")
introncds.grid(row = rowflag, column = 2, sticky = "W")
rowflag += 1

#内含子线型
intronLabel = tk.Label(PGS, text = "内含子线型:")
intronLabel.grid(row = rowflag, column = 0, sticky = "E", padx = 10)
intronvar = tk.StringVar()
intronvar.set("straight")
intronstraight = tk.Radiobutton(PGS, variable = intronvar, text = "直线", value = "straight")
intronstraight.grid(row = rowflag, column = 1, sticky = "W")
intronbroken = tk.Radiobutton(PGS, variable = intronvar, text = "折线", value = "broken")
intronbroken.grid(row = rowflag, column = 2, sticky = "W")
rowflag += 1

#长度指定
kblenLabel = tk.Label(PGS, text = "每kb图像长度(px):", padx = 10)
kblenLabel.grid(row = rowflag, column = 0, sticky = "E")
kbEn = tk.StringVar()
kbEn.set("250")
kbEntry = tk.Entry(PGS, textvariable = kbEn, width = 50)
kbEntry.grid(row = rowflag, column = 1, sticky = "WE", columnspan = 5)
tk.Label(PGS, text = "默认: 250px/kb").grid(row = rowflag, column = 6, sticky = "W")
rowflag += 1

#颜色指定
colorLabel = tk.Label(PGS, text = "颜色指定:", padx = 10)
colorLabel.grid(row = rowflag, column = 0, sticky = "E")
colorEn = tk.StringVar()
colorEntry = tk.Entry(PGS, textvariable = colorEn, width = 50)
colorEntry.grid(row = rowflag, column = 1, sticky = "WE", columnspan = 5)
tk.Label(PGS, text = "默认: 内置方案。"
         ).grid(row = rowflag, column = 6, sticky = "W")
tk.Label(PGS, text = "定义方法如: CDS:green;UTR:red;LRR:yellow;..."
         ).grid(row = rowflag + 1, column = 6, columnspan = 4, sticky = "W")
rowflag += 2

#运行程序
tk.Button(PGS, text = "开始绘制", command = StartPainting, padx = 10
          ).grid(row = rowflag, column = 1, columnspan = 5, sticky = "WE")

#添加demo图
photo = tk.PhotoImage(file='example.gif')
label = tk.Label(PGS, image=photo)
label.image = photo
label.grid(row=8, column=8, columnspan=4, rowspan=9, sticky="WE", padx=5, pady=5)
tk.Label(PGS,text= "推荐使用开源免费软件Inkscape对图像进行后续处理\nhttps://inkscape.org"
         ).grid(row = 11, column = 1, columnspan = 5, rowspan = 3, sticky = "E")

PGS.mainloop()


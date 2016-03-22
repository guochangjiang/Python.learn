#!/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
将指定列表中文件(附带绝对路径)拷贝到指定文件夹下，用法为:
    xx.py list.filr target.dir
(该程序会把同名文件进行重命名)
"""

import os
import sys

filedict = {}
filelist = []

#判断目标文件是否存在
if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

#生成log文件
LogFile = open("copy.files.in.list.log", 'w')

#处理文件数目
copyfilenum = 0

with open(sys.argv[1], "r") as LIST:
    for line in LIST:
        line = line.strip()
        if line == "":
            continue
        print("copying", line)
        filename = os.path.basename(line)
        if  filename not in filelist:
            filedict[filename] = 1
            filelist.append(filename)
            os.system('cp -f "' + line + '" "' + sys.argv[2] + filename + '"')
            LogFile.write(line + "\n\t----->" + sys.argv[2] + filename + "\n")
            copyfilenum += 1
        else:
            print("\tsame file!!!", filename)
            filedict[filename] += 1
            os.system('cp -f "' + line + '" "' + sys.argv[2] + filename + '2"')
            LogFile.write(line + "\n\t----->" + sys.argv[2] + filename + "2\n")
            copyfilenum += 1

print("##################")
print("处理文件数目: %d" % copyfilenum)
LogFile.close()
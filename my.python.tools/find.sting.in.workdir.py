#!/usr/bin/env python3
# -*-coding: utf-8-*-

'''
在当前目录下搜索指定格式文件，并查找指定字符串
'''

import os
import re


filenamelist=os.listdir(os.getcwd())
for file in filenamelist:
    if re.search("(\.php$)|(\.html$)", file):
        print("Searching file", file, "........")
        with open(file, "r") as INFILE:
            for line in INFILE:
                line = line.strip()
                if re.search("\.html",line):
                    print("\t",line)
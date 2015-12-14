#!/usr/bin/env python3
# --*-- utf-8 --*--
#===============================================================================
#
#         FILE: Reverse.DNA.py
#
#        USAGE: 直接运行程序即可
#
#  DESCRIPTION: 该程序从剪切板中获取DNA/RNA序列(可包含简并碱基)
#               并将其互补序列拷贝到剪切板中
#
#      OPTIONS: ---
# REQUIREMENTS: 将要反转的DNA/RNA序列复制到剪切板中
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/09/07 12:47:14
#     REVISION: ---
#===============================================================================

import pyperclip
import re
import os


DNAseq = pyperclip.paste()
DNAseq = DNAseq.upper()
DNAseq = re.sub("\s+", "", DNAseq)
DNAseq = re.sub("\n", "", DNAseq)
DNAseq = DNAseq.strip()

print("The origin sequence is:")
print(DNAseq)

#length = len(DNAseq)
DNA_rev = ''

if re.search(r"U", DNAseq):
    DNAseq = re.sub("A", "X", DNAseq)

DNAseq = DNAseq[::-1]
#print("DNAseq: ", DNAseq)
#print("DNA_rev: ", DNA_rev)

for base in DNAseq:
    #print("base: ", base)
    if base == 'A':
        DNA_rev = DNA_rev + 'T'
    elif base == 'G':
        DNA_rev = DNA_rev + 'C'
    elif base == 'C':
        DNA_rev = DNA_rev + 'G'
    elif base == 'T':
        DNA_rev = DNA_rev + 'A'
    elif base == 'U':
        DNA_rev = DNA_rev + 'A'
    elif base == 'X':
        DNA_rev = DNA_rev + 'U'
    elif base == 'R':
        DNA_rev = DNA_rev + 'Y'
    elif base == 'W':
        DNA_rev = DNA_rev + 'W'
    elif base == 'S':
        DNA_rev = DNA_rev + 'S'
    elif base == 'Y':
        DNA_rev = DNA_rev + 'R'
    elif base == 'K':
        DNA_rev = DNA_rev + 'M'
    elif base == 'M':
        DNA_rev = DNA_rev + 'K'
    elif base == 'V':
        DNA_rev = DNA_rev + 'B'
    elif base == 'B':
        DNA_rev = DNA_rev + 'V'
    elif base == 'H':
        DNA_rev = DNA_rev + 'D'
    elif base == 'D':
        DNA_rev = DNA_rev + 'H'
    elif base == 'N':
        DNA_rev = DNA_rev + 'N'
    else:
        print ("Abnormal base is found!! It's", base)
    #print("DNA_rev: ", DNA_rev)

print("------------\n\nThe complementary sequence:")
print(DNA_rev)
#clear = ''
#clipboard.copy(clear)
pyperclip.copy(DNA_rev)

os.system('pause')




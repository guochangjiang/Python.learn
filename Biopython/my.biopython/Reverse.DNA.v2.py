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
#        NOTES: 将碱基替代用字典方式进行
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 2.0
#      CREATED: 2015/09/07 12:47:14
#     REVISION: ---
#===============================================================================

import pyperclip
import re
import os

BaseData = {
    'A': 'T',
    'T': 'A',
    'G': 'C',
    'C': 'G',
    'U': 'A',
    'X': 'U',
    'R': 'Y',
    'Y': 'R',
    'W': 'W',
    'S': 'S',
    'M': 'K',
    'K': 'M',
    'V': 'B',
    'B': 'V',
    'H': 'D',
    'D': 'H',
    'N': 'N'
}
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
    if base in BaseData.keys():
        DNA_rev += BaseData[base]
    else:
        print ("Abnormal base is found!! It's", base)
    #print("DNA_rev: ", DNA_rev)

print("------------\n\nThe complementary sequence:")
print(DNA_rev)
#clear = ''
#clipboard.copy(clear)
pyperclip.copy(DNA_rev)

os.system('pause')




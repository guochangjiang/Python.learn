#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: calculate.Pi.v1.0.py
#
#        USAGE: -in aln.fasta -out output.csv
#
#  DESCRIPTION: 计算指定fasta(Align DNA)文件的Pi值(MEGA)
#
#      OPTIONS: ---
# REQUIREMENTS: 至少两条序列
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/11/02 14:42:00
#       UPDATE: 2015/11/02 14:42:00
#===============================================================================
#   Change logs:
#   Version 1.o: 初始版本: 支持二倍体简并碱基计算

__version__ = '1.0'

import re
import os
from os.path import getsize
import math

#子例程
#获取简并碱基对应碱基
def Get_Degenerate_Base(base):
    if base == 'M':
        return('A', 'C')
    elif base == 'R':
        return ('A', 'G')
    elif base == 'W':
        return ('A', 'T')
    elif base == 'S':
        return ('C', 'G')
    elif base == 'Y':
        return ('C', 'T')
    elif base == 'K':
        return ('T', 'G')
    elif base == 'V':
        return ('A', 'C', 'G')
    elif base == 'H':
        return ('A', 'C', 'T')
    elif base == 'D':
        return ('A', 'T', 'G')
    elif base == 'B':
        return ('T', 'C', 'G')
    else:
        print("Error base: %s" %base)
        return('-',)




##参数处理
import argparse
parser = argparse.ArgumentParser(
        description="本程序用于已比对DNA fasta文件的核苷酸差异度Pi计算。\nVersion: " + __version__,
        epilog="Please Enjoy this Program!")
parser.add_argument(
        "-i", "-in", "--input",
        metavar="fasta_file",
        dest="fasta_in",
        required=True,
        type=str,
        help="fasta file to calculate Pi")
parser.add_argument(
        "-o", "-out", "--output",
        metavar="out_file",
        dest="file_out",
        type=str,
        default='pi.value.tmp.csv',
        help="csv file to output Pi info")
parser.add_argument(
        "-v", "--version",
        action='version',
        help="The version of this program.",
        version = "Version: " + __version__)
args = parser.parse_args()

print("do file:", args.fasta_in, "........", end='')
locus_list = []
Allseq_dict = {}
seq_name = ''
with open(args.fasta_in, 'r') as Data_in:
    for line in Data_in:
        line =  line.strip()
        if line == '':
            continue
        if line[0] == ">":
            seq_name = line[1:]
            if seq_name not in locus_list:
                locus_list.append(seq_name)
                Allseq_dict[seq_name] = ''
        else:
            Allseq_dict[seq_name] += line

OUTPUT = open(args.file_out, "w")
fas_id = args.fasta_in
filesize = getsize(args.fasta_in)
if filesize == 0 or locus_list == [] or len(locus_list) < 2:
    print("输入文件不合要求，请检查！")
    OUTPUT.write("#" + fas_id + ",-\n")
    os.exit(0)

pi_list = []
pi_dict = {}
name = ""
count = 0
sum_pi = 0

for i in range(len(locus_list)):
    for j in range(i+1, len(locus_list)):
        e_length = 0 # 两条序列重叠部分碱基总数
        d_length = 0 # 两条序列重叠部分不同碱基总数
        seq1 = Allseq_dict[locus_list[i]].upper()
        seq2 = Allseq_dict[locus_list[j]].upper()
        for index in range(len(seq1)):
            base1 = seq1[index]
            base2 = seq2[index]
            if base1 in "ATCGMRWSYKVHDB" and base2 in "ATCGMRWSYKVHDB":
                e_length += 1
                if base1 in 'ATCG' and base2 in 'ATCG' and base1 != base2:
                    d_length += 1
                if base1 in 'ATCG' and base2 in 'MRWSYKVHDB':
                    bases = Get_Degenerate_Base(base2)
                    same = 0
                    for b in bases:
                        if b == base1:
                            same += 1
                    if same == 0:
                        d_length += 1
                if base2 in 'ATCG' and base1 in 'MRWSYKVHDB':
                    bases = Get_Degenerate_Base(base1)
                    same = 0
                    for b in bases:
                        if b == base2:
                            same += 1
                    if same == 0:
                        d_length += 1
                if base1 in "MRWSYKVHDB" and base2 in "MRWSYKVHDB":
                    bases1 = Get_Degenerate_Base(base1)
                    bases2 = Get_Degenerate_Base(base2)
                    same = 0
                    for b1 in bases1:
                        for b2 in bases2:
                            if b1 == b2:
                                same += 1
                    if same == 0:
                        d_length += 1
                    elif same == 1:
                        d_length += 0.5
                    else:
                        pass
        if e_length == 0:
            pi_list.append('-')
        else:
            pi = d_length / e_length
            pi = (-3/4)*math.log(1-(4/3)*pi)
            pi_list.append(pi)
            sum_pi += pi
            count += 1

aver_pi = sum_pi / count
OUTPUT.write("#%s, average=%s\n" % (fas_id, str(aver_pi)))
for locus in locus_list:
    OUTPUT.write(locus + ",")
OUTPUT.write("\n")
for index in range(len(locus_list)-1):
    OUTPUT.write(locus_list[index])
    slipper = "," * (index+1)
    OUTPUT.write(slipper)
    for i in range(len(locus_list)-index-1):
        OUTPUT.write(str(pi_list[0]) + ",")
        pi_list = pi_list[1:]
    OUTPUT.write("\n")
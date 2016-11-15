#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: calculate.Pi.between.2.fas.v1.1
#
#        USAGE: -in aln.fasta -out output.csv
#
#  DESCRIPTION: 计算指定2个fasta(Align DNA)文件的Pi值(MEGA)(Dxy)
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
        "-i1", "-in1", "--input1",
        metavar="fasta_file_1",
        dest="fasta_in_1",
        required=True,
        type=str,
        help="first fasta file to calculate Pi")
parser.add_argument(
        "-i2", "-in2", "--input2",
        metavar="fasta_file_2",
        dest="fasta_in_2",
        required=True,
        type=str,
        help="second fasta file to calculate Pi")

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

print("do file:", args.fasta_in_1, "vs", args.fasta_in_2, "........", end='')
locus_list_1 = []
seq_dict_1 = {}
seq_name = ''
with open(args.fasta_in_1, 'r') as Data_in:
    for line in Data_in:
        line =  line.strip()
        if line == '':
            continue
        if line[0] == ">":
            seq_name = line[1:]
            if seq_name not in locus_list_1:
                locus_list_1.append(seq_name)
                seq_dict_1[seq_name] = ''
        else:
            seq_dict_1[seq_name] += line
locus_list_2 = []
seq_dict_2 = {}
seq_name = ''
with open(args.fasta_in_2, 'r') as Data_in:
    for line in Data_in:
        line =  line.strip()
        if line == '':
            continue
        if line[0] == ">":
            seq_name = line[1:]
            if seq_name not in locus_list_2:
                locus_list_2.append(seq_name)
                seq_dict_2[seq_name] = ''
        else:
            seq_dict_2[seq_name] += line

OUTPUT = open(args.file_out, "w")
fas_id = args.fasta_in_1 + "&" + args.fasta_in_2
filesize_1 = getsize(args.fasta_in_1)
filesize_2 = getsize(args.fasta_in_2)
if filesize_1 == 0 or filesize_2 == 0 or locus_list_1 == [] or len(locus_list_1) < 2 or locus_list_2 == [] or len(locus_list_2) < 2:
    print("输入文件不合要求，请检查！")
    OUTPUT.write("#" + fas_id + ",-\n")
    os.exit(0)

pi_list = []
pi_dict = {}
name = ""
count = 0
sum_pi = 0

flag = 0
for locus_1 in locus_list_1:
    flag += 1
    print(locus_1, flag, "/", len(locus_list_1))
    for locus_2 in locus_list_2:
        e_length = 0 # 两条序列重叠部分碱基总数
        d_length = 0 # 两条序列重叠部分不同碱基总数
        seq1 = seq_dict_1[locus_1].upper()
        seq2 = seq_dict_2[locus_2].upper()
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

OUTPUT.write(",")
for locus in locus_list_2:
    OUTPUT.write(locus + ",")
OUTPUT.write("\n")
for index in range(len(locus_list_1)-1):
    OUTPUT.write(locus_list_1[index])
    for i in range(index*len(locus_list_2),(index+1)*len(locus_list_2)):
        OUTPUT.write(str(pi_list[i]) + ",")
    OUTPUT.write("\n")
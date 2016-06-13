#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#  DESCRIPTION: 计算当前文件下所有符合匹配模式的fasta(Align DNA)文件的平均Pi值(MEGA)
#
#      OPTIONS: -glob *.fas -out out.csv
# REQUIREMENTS: 每个文件至少两条序列
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/11/02 14:42:00
#       UPDATE: 2015/11/02 14:42:00
#===============================================================================
#   Change logs:
#   Version 1.0: 初始版本： 计算指定fasta文件（可以是多个）的平均Pi值

__version__ = '1.0'

import re
import os
import glob
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
        "-g", "-glob", "--glob",
        metavar="fasta_files",
        dest="glob_key",
        default='*.aln.fas',
        type=str,
        help="glob key of fasta files to calculate Pi, [default: *.aln.fas]")
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

OUTPUT = open(args.file_out, "w")
filenum = 0

all_files = glob.glob(args.glob_key)
file_all_num = len(all_files)
for fas_file in all_files:
    filenum += 1
    print("do file:", fas_file, "...... (%d/%d)" % (filenum, file_all_num))
    sample_list = []
    locus_list = []
    Allseq_dict = {}
    sample_seq_dict = {}
    seq_name = ''
    with open(fas_file, 'r') as Data_in:
        for line in Data_in:
            line =  line.strip()
            if line == '':
                continue
            if line[0] == ">":
                seq_name = line[1:]
                if seq_name not in locus_list:
                    locus_list.append(seq_name)
                    Allseq_dict[seq_name] = ''
                m = re.search("\|(.+)$", seq_name)
                sample = m.group(1)
                if sample not in sample_list:
                    sample_list.append(sample)
                    sample_seq_dict[sample] = []
            else:
                Allseq_dict[seq_name] += line
    for key in Allseq_dict.keys():
        m = re.search("\|(.+)$", key)
        sample_seq_dict[m.group(1)].append(Allseq_dict[key])
    filesize = getsize(fas_file)
    if filesize == 0 or locus_list == [] or len(locus_list) < 2:
        print("输入文件不合要求，请检查！")
        OUTPUT.write("#" + fas_file + ",-\n")
        os.exit(0)
    #开始计算Pi
    name = ""
    count = 0
    sum_pi = 0
    pair_num = 0
    processing_num = 1
    for i in range(len(sample_list)):
        #print("Sample:", sample_list[i])
        for j in range(i+1, len(sample_list)):
            total_pair = len(sample_list) * (len(sample_list)-1) / 2
            print("Process rate: %d / %d\r" % (processing_num, total_pair), end = '')
            processing_num += 1
            pair_num += 1
            pi_num = 0
            pi_sum = 0
            for seq1 in sample_seq_dict[sample_list[i]]:
                for seq2 in sample_seq_dict[sample_list[j]]:
                    e_length = 0 # 两条序列重叠部分碱基总数
                    d_length = 0 # 两条序列重叠部分不同碱基总数
                    seq1 = seq1.upper()
                    seq2 = seq2.upper()
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
                        pass
                    else:
                        pi = d_length / e_length
                        pi = (-3/4)*math.log(1-(4/3)*pi)
                        pi_num += 1
                        pi_sum += pi
            if pi_num == 0:
                pass
            else:
                count += 1
                sum_pi += pi_sum / pi_num
    
    aver_pi = sum_pi / count
    OUTPUT.write("#" + fas_file + ",%s\n" %str(aver_pi))
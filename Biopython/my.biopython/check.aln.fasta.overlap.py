#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
检测比对过的fasta文件中所有序列之间是否两两均具有重叠区域
'''

__version__ = "1.0"

from pyfasta import Fasta
import argparse

#命令行选项处理
parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="filename", dest="input", type=str , help="fasta file to check")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()

f = Fasta(args.input)
loci = sorted(f.keys())
for locus1 in loci:
    for locus2 in loci:
        flag = 0
        sequence1 = f[locus1]
        sequence2 = f[locus2]
        i = 0
        while i < len(sequence1) and i < len(sequence2):
            base1 = sequence1[i]
            base2 = sequence2[i]
            if base1 != "-" and base2 != "-":
                flag = 1
                break
            i += 1
        if flag == 0:
            print(locus1, "与", locus2, "不存在重叠序列！")
        else:
            print(locus1, "与", locus2, "存在重叠序列！")
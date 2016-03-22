#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
#===============================================================================
#
#         FILE: get.seq.by.namelist.from.fasta.py
#
#        USAGE: usage
#
#  DESCRIPTION: 根据指定位点列表在fasta文件中获取所有序列
#
#      OPTIONS: -in fasta.file -name name.file -out out.fasta.file
# REQUIREMENTS:
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0.0
#      CREATED: 2015/10/22 15:35:10
#      UPDATE:  2015/10/22 15:35:10
#===============================================================================
#   Change logs:
#   Version 1.0.0 2016/3/18: The initial version.

__version__ = '1.0.0'

import re
import argparse
from pyfasta import Fasta

parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="filename", dest="input_file", type=str, required=True, help="fasta file to input")
parser.add_argument("-o", "-out", "--output", metavar="filename", dest="out_file", type=str, required=True, help="fasta file to output")
parser.add_argument("-name", "--name", metavar="namefile", dest="loci_list_file", type=str, required=True, help="the file of loci list")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()
#print(args)
#print(args.input_file)
#print(args.out_file)
output = open(args.out_file, 'w')

#读取fasta文件
print("%s文件读取中" % args.input_file)
f = Fasta(args.input_file)

with open(args.loci_list_file, 'r') as LIST:
    for locus in LIST:
        locus = locus.strip()
        if locus == "":
            continue
        print(locus)
        output.write(">%s\n" % locus)
        output.write("%s\n" % f[locus])

output.close()
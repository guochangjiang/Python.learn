#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: get.seq.by.name.v1.py
#
#        USAGE: usage
#
#  DESCRIPTION: 根据指定的名字关键字在fasta文件中找到包含该关键词的所有序列
#
#      OPTIONS: -in fasta.file -name keyword -out out.fasta.file
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
#   Version 1.0.0 2015/10/22: The initial version.

__version__ = '1.0.0'

import re
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="filename", dest="input_file", type=str , help="fasta file to input")
parser.add_argument("-o", "-out", "--output", metavar="filename", dest="out_file", type=str , help="fasta file to output")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
parser.add_argument("-name", "--name", metavar="keyword", dest="sequence name", type=str, help="the keyword of the sequence name")
args = parser.parse_args()


output = open(args.out, 'w')

print()
for seq_record in SeqIO.parse(args.input, "fasta"):
    #print("Processing", seq_record.id, "............")
    if re.match(args.name, seq_record.id):
        output.write(">")
        output.write(seq_record.id)
        output.write("\n")
        output.write(seq_record.seq)
        output.write("\n")

output.close()


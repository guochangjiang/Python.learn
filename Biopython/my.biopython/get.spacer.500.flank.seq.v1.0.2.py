#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: get.sapcer.500.flank.seq.py
#
#        USAGE: usage
#
#  DESCRIPTION: 根据剪切板中的spacer序列获取其在基因组的500bp侧翼序列
#
#      OPTIONS: ---
# REQUIREMENTS:
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0.2
#      CREATED: 2015/10/15 15:35:10
#      UPDATE:  2015/10/16 15:35:10
#===============================================================================
#   Change logs:
#   Version 1.0.0 2015/10/16: The initial version.
#	Version 1.0.1 2015/10/16: use Biopython to get fasta data
#	Version 1.0.2 2015/10/16: replace getopt by optparse 

__version__ = '1.0.2'

import pyperclip
import re
import os
import argparse
import sys
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Process some options (head).', epilog="This is a usage of %(prog)s [end]")
parser.add_argument("-i", "-in", "--input", metavar="filename", dest="input_file", type=str , help="fasta file to input")
parser.add_argument("-o", "-out", "--output", metavar="filename", dest="out_file", type=str , help="fasta file to output")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()


spacer = pyperclip.paste()
spacer = spacer.upper()
spacer = re.sub("\s+", "", spacer)
spacer = re.sub("\n", "", spacer)
#print(spacer[21:23])
#print(len(spacer))

if spacer[21:23] == "GG" and len(spacer) == 23:
    print("The spacer sequence is:")
    print(spacer)
else:
    print("Spacer Error!!!")
    os._exit(0)

spacer_rev = spacer[::-1]
spacer_rev = re.sub("G", "c", spacer_rev)
spacer_rev = re.sub("C", "g", spacer_rev)
spacer_rev = re.sub("A", "t", spacer_rev)
spacer_rev = re.sub("T", "a", spacer_rev)
spacer_rev = spacer_rev.upper()

output = open(args.out, 'w')

print()
for seq_record in SeqIO.parse(args.input, "fasta"):
    print("Processing", seq_record.id, "............")
    length = len(seq_record)
    i = 0
    while (i <= length - 23):
        subseq = seq_record.seq[i:i+23]
        if subseq == spacer or subseq == spacer_rev:
            start = i - 500
            end = i+523
            if start < 0:
                start = 0
            if end > length-1:
                end = length-1
            flank_seq = seq_record.seq[start:end]
            output.write(">")
            output.write(seq_record.id)
            output.write("-")
            output.write(str(i))
            output.write("\n")
            output.write(str(flank_seq))
            output.write("\n")
        i = i + 1
output.close()


#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: calculate.Pi.v1.0.py
#
#        USAGE: usage
#
#  DESCRIPTION: 计算指定fasta(Align DNA)文件的Pi值(MEGA)
#
#      OPTIONS: ---
# REQUIREMENTS: 需要每条序列仅占一行
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/11/02 14:42:00
#       UPDATE: 2015/11/02 14:42:00
#===============================================================================
#   Change logs:
#   Version

__version__ = '1.0'

import re
import os
from os.path import getsize

##参数处理
import argparse
parser = argparse.ArgumentParser(
        description="本程序用于已比对DNA fasta文件的核苷酸差异度Pi计算。\nVersion: " + __version__,
        epilog="Please Enjoy this Program!")
parser.add_argument(
        "-i", "-in", "--input",
        metavar="fastafile",
        dest="input",
        type=str,
        help="fasta file to calculate Pi")
parser.add_argument(
        "-v", "--version",
        action='version',
        help="The version of this program.",
        version = "Version: " + __version__)
args = parser.parse_args()

print("do file:", args.input, "........", end='')
Datain = open(args.input, 'r')
Allseq = []
for line in Datain:
    line =  line.strip()
    if line =='':
        continue
    Allseq.append(line)
Datain.close()

outfile = re.sub("\.fas.*", ".Pi.value.csv", args.input)
OUTPUT = open(outfile, "w")
id = "default"
if LOC in args.input:
    match = re.search("(LOC_Os\d+g\d+\.\d+)", args.input)
    id = match.group(1)

filesize = getdirsize(args.input)
if filesize == 0 or len(Allseq):
    OUTPUT.write("#" + id + ",-\n")
    os.exit(0)



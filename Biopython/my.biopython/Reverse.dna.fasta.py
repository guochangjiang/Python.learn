#!/usr/bin/env python3
# --*-- utf-8 --*--
#===============================================================================
#
#         FILE: Reverse.DNA.fasta.py
#
#        USAGE: python Reverse.DNA.fasta.py -i in.fasta -o out fasta
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
#      VERSION: 1.0.0
#      CREATED: 2015/09/07 12:47:14
#     REVISION: ---
#===============================================================================

import re

__version__ = "1.0.0"

#命令行参数处理
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="fasta_in", dest="fasta_in", type=str , required=True, help="fasta file to reverse&complement")
parser.add_argument("-o", "-out", "--output", metavar="fasta_out", dest="fasta_out", type=str, help="fasta file to output, [default: inputfile.reverse.fasta]")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()

def ReverseComplement(DNAseq)
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
        'N': 'N',
        '-': '-',
    }
    DNAseq = DNAseq.upper()
    DNAseq = re.sub("\s+", "", DNAseq)
    DNAseq = re.sub("\n", "", DNAseq)
    DNAseq = DNAseq.strip()
    DNA_rev = ''
    if re.search(r"U", DNAseq):
        DNAseq = re.sub("A", "X", DNAseq)
    DNAseq = DNAseq[::-1]
    for base in DNAseq:
        if base in BaseData.keys():
            DNA_rev += BaseData[base]
        else:
            print("Abnormal base is found!! It's", base)
    return DNA_rev

#主程序
fasta_in = args.fasta_in
try:
    fasta_out = args.fasta_out
except:
    fasta_out = fasta_in.replace("fasta","reverse.fasta")

OUT = open(fasta_out,"w")
with open(fasta_in) as IN:
    for line in IN:
        line = line.strip()
        if line == '':
            continue
        if line[0] == '>':
            OUT.write(line + "\n")
        else:
            OUT.write(ReverseComplement(line) + "\n")
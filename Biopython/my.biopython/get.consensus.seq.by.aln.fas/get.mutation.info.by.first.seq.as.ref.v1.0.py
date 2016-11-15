#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
根据比对好的氨基酸序列，以第一条序列为reference对各个位置的突变情况进行统计
'''

__version__ = '1.0'

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="filename", dest="in_file", type=str, help="aligned fasta file to input")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="tmp.mutation.seq.out",
                    type=str,
                    help=".out file to output, [default: tmp.txt]")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version="Version: " + __version__)
args = parser.parse_args()

chromosome = "chr"
gene_name_list = []
gene_seq_dict = {}

with open(args.in_file) as FAS:
    gene_name = ''
    for line in FAS:
        line = line.strip()
        if line == '':
            continue
        if line[0] == '>':
            gene_name = line[1:]
            if gene_name in gene_name_list:
                print("Not uniq gene name:", gene_name)
                gene_seq_dict[gene_name] = ''
                continue
            else:
                gene_name_list.append(gene_name)
                gene_seq_dict[gene_name] = ''
        else:
            gene_seq_dict[gene_name] += line

#检查序列长度是否一致
seq_length = len(gene_seq_dict[gene_name_list[0]])
for gene in gene_name_list[1:]:
    if len(gene_seq_dict[gene]) != seq_length:
        print("sequences are not aligned!")
        os._exit(0)

#生成突变信息
OUT = open(args.file_out, 'w')
OUT.write("%s\t%s" %("reference", chromosome))
for i in range(seq_length):
    OUT.write("\t.")
OUT.write("\n")

for gene in gene_name_list[1:]:
    OUT.write("%s\t%s" %(gene, chromosome))
    for i in range(seq_length):
        base_ref = gene_seq_dict[gene_name_list[0]][i].upper()
        base_cur = gene_seq_dict[gene][i].upper()
        if base_ref != '-' and base_cur == '-':
            OUT.write("\tDEL")
        elif base_ref == '-' and base_cur != '-':
            OUT.write("\tINS")
        elif base_ref == base_cur:
            OUT.write("\t.")
        else:
            OUT.write("\tMUT")
    OUT.write("\n")
OUT.close()
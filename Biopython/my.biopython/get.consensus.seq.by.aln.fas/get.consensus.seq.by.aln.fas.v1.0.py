#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.consensus.seq.by.aln.fas.v1.0.py
       USAGE: $ python get.consensus.seq.by.aln.fas.v1.0.py -h
 DESCRIPTION: get the consensus sequence from aligned fasta file
     OPTIONS: -in aln.fas -out consensus.sequence.csv
REQUIREMENTS: aligned fasta file
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/11/9 19:05:04
      UPDATE: 2016/11/9 19:05:04

 CHANGE LOGS:
     Version 1.0 2016/11/9 19:05:04    初始版本
'''

import argparse
import os

# 子例程
# 按数目从多到少输出字符串中的字符
def Sort_Char_by_Num(seq_str):
    char_dict = {}
    for char in seq_str:
        if char not in char_dict:
            char_dict[char] = 0
        char_dict[char] += 1
    #按值降序排序，在值相等的情况下再按键升序排序
    sort_kv = sorted(char_dict.items(), key=lambda kv: (-kv[1], kv[0]))
    sort_chars = ''
    for kv in sort_kv:
        sort_chars += kv[0]
    return(sort_chars)


__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-i",
                    "-in",
                    "--input",
                    metavar="input_file",
                    dest="fasta_in",
                    required=True,
                    type=str,
                    help="file to input")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="tmp.consensus.seq.csv",
                    type=str,
                    help="file to output, [default: tmp.txt]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

gene_list = []      #序列名列表
gene_seq_dict = {}  #序列字典

#读取fasta序列
with open(args.fasta_in) as FAS:
    name = ''
    for line in FAS:
        line = line.strip()
        if line == '':
            continue
        if line[0] == ">":
            name = line[1:]
            if name in gene_list:
                print("Not uniq name:", name)
            else:
                gene_list.append(name)
            gene_seq_dict[name] = ''
        else:
            gene_seq_dict[name] += line

#序列长度检查
seq_length = len(gene_seq_dict[gene_list[0]])
for seq in gene_seq_dict.values():
    if len(seq) != seq_length:
        print("Please make sure the length of all sequence is the same!")
        os._exit(0)

pos_base_str_list = []      #按位置将碱基存储到列表
seq_num = len(gene_list)
for i in range(seq_length):
    pos_base_str_list.append('')
    for j in range(seq_num):
        pos_base_str_list[i] += gene_seq_dict[gene_list[j]][i]

consensus_seq = ''  #一致序列
for seq in pos_base_str_list:
    base_max = Sort_Char_by_Num(seq)
    #consensus_seq += ","
    consensus_seq += base_max[0]

OUT = open(args.file_out, "w")
OUT.write("consensus")
for base in consensus_seq:
    OUT.write("," + base)
OUT.write("\n")

for gene in gene_list:
    out_str = ''
    for i in range(seq_length):
        if gene_seq_dict[gene][i] == consensus_seq[i]:
            out_str += '.'
        else:
            out_str +=gene_seq_dict[gene][i]
    OUT.write(gene)
    for base in out_str:
        OUT.write("," + base)
    OUT.write("\n")
OUT.close()
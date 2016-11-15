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
     Version 1.1 2016/11/9 20:20:04    输出格式从csv改为excel
'''

import argparse
import os
import xlsxwriter as wx

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
# 26进制转换
def Num_2_AZ(num):
    twenty_six_dic = {  1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',
                        7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',
                        13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',
                        19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',
                        25:'Y',26:'Z'}
    remainder_str = ''
    while num  >= 1:
        rem = num % 26
        num = int(num/26)
        if rem == 0:
            rem = 26
            num = num - 1
        remainder_str += twenty_six_dic[rem]
    return(remainder_str[::-1])

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
                    default="tmp.consensus.seq.xlsx",
                    type=str,
                    help="excel file to output, [tmp.consensus.seq.xlsx]")
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

excel_name = args.file_out
workbook = wx.Workbook(excel_name)
worksheet = workbook.add_worksheet()
end_column = Num_2_AZ(1+seq_length)
column_range = "B:%s" %end_column
worksheet.set_column(column_range, 2)

row_1 = ['consensus'] + list(consensus_seq)
worksheet.write_row('A1', row_1)

column_count = 1
for gene in gene_list:
    out_str = ''
    column_count += 1
    for i in range(seq_length):
        if gene_seq_dict[gene][i] == consensus_seq[i]:
            out_str += '.'
        else:
            out_str +=gene_seq_dict[gene][i]
    row_out = [gene] + list(out_str)
    worksheet.write_row('A'+str(column_count), row_out)
workbook.close()
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.domain.info.by.namelist.from.pfam.v1.0.py
       USAGE: $ python get.domain.info.by.namelist.from.pfam.v1.0.py -h
 DESCRIPTION: 按指定文件中包含的基因列表从相应的pfam文件中获取每个基因的
              domain信息，如提供基因或蛋白fasta文件，亦可输出相应的氨基酸
              长度信息，输出格式为：gene_id domain start end domain_name
              (其实，本程序用于生成可进行蛋白结构图绘制的蛋白质结构域信息文件)
     OPTIONS: -namefile [namelist] -fasta [cds/protein fasta] -pfam [pfamfile]
REQUIREMENTS:
        BUGS:
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/3/24 15:07:17
      UPDATE: 2016/3/24 15:07:17

 CHANGE LOGS:
     Version 1.0 2016/3/24 15:07:17    初始版本
'''

import argparse
import re

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-nf",
                    "--namefile",
                    metavar="name_file",
                    dest="name_infile",
                    required=True,
                    type=str,
                    help="file of name list to input")
parser.add_argument(
                    "-p",
                    "--pfamfile",
                    metavar="pfam_file",
                    dest="pfam_infile",
                    required=True,
                    type=str,
                    help="file of pfam to input")
parser.add_argument(
                    "-fasta",
                    "--genefasta",
                    metavar="fasta_file",
                    dest="fasta_infile",
                    default="None",
                    type=str,
                    help="file of fasta to input")
parser.add_argument(
                    "-ft",
                    "--fastatype",
                    metavar="fasta_type",
                    dest="fasta_type",
                    default="protein",
                    type=str,
                    help="type of fasta, e.g. protein, DNA [default:p protein]")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="tmp.txt",
                    type=str,
                    help="file to output, [default: tmp.txt]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

name_list = []
with open(args.name_infile) as NL:
    for line in NL:
        line = line.strip()
        if line == "":
            continue
        name_list.append(line)

gene_len_dict = {}
fasta_flag = 0
fasta_type = args.fasta_type
gene_name = ''
if args.fasta_infile == "None":
    pass
else:
    fasta_flag = 1
    with open(args.fasta_infile) as FAS:
        for line in FAS:
            line = line.strip()
            if line == "":
                continue
            if line[0] == ">":
                for name in name_list:
                    if name in line:
                        gene_name = name
                        gene_len_dict[gene_name] = 0
                        break
                    else:
                        gene_name = ''
            else:
                if gene_name == '':
                    continue
                line = re.sub("\s+", "", line)
                line = line.upper()
                if fasta_type == "protein":
                    gene_len_dict[gene_name] += len(line)
                    # print(">%s\n%s" %(gene_name, line))
                else:
                    gene_len_dict[gene_name] += len(line)/3.0

gene_pfam_dict = {}
gene_max_len = {}
pfam_gene_list = []
with open(args.pfam_infile) as PFAM:
    for line in PFAM:
        line = line.strip()
        if line == "" or line[0] == "#":
            continue
        columns = line.split()
        for name in name_list:
            if name in columns[0]:
                if name not in pfam_gene_list:
                    gene_pfam_dict[name] = []
                    gene_pfam_dict[name].append(columns[1] + "\t" + columns[2] + "\t" + columns[6])
                    gene_max_len[name] = int(columns[2])
                    pfam_gene_list.append(name)
                else:
                    gene_pfam_dict[name].append(columns[1] + "\t" + columns[2] + "\t" + columns[6])
                    if gene_max_len[name] < int(columns[2]):
                        gene_max_len[name] = int(columns[2])
                break

OUT = open(args.file_out, "w")
for gene in sorted(name_list):
    if gene not in pfam_gene_list:
        print("%s no domain found!!!" % gene)
    else:
        if fasta_flag == 1:
            OUT.write("%s\tprotein\t1\t%s\t-\n" % (gene, int(gene_len_dict[gene])))
            for line in gene_pfam_dict[gene]:
                OUT.write("%s\tdomain\t%s\n" % (gene, line))
        else:
            OUT.write("%sprotein\t1\t%s\t-\n" % (gene, gene_max_len[gene]))
            for line in gene_pfam_dict[gene]:
                OUT.write("%s\tdomain\t%s\n" % (gene, line))
OUT.close()

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: tranfer.gene.id.between.RAP_MSU.gene.py
       USAGE: $ python tranfer.gene.id.between.RAP_MSU.gene.py -h
 DESCRIPTION: 在RAP与MSU基因编号之间进行相互转换，可指定列表文件或者位点
     OPTIONS: options
REQUIREMENTS: requirements
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/3/28 20:06:48
      UPDATE: 2016/3/28 20:06:48

 CHANGE LOGS:
     Version 1.0 2016/3/28 20:06:48    初始版本
'''

import argparse
import re

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-i",
                    "-in",
                    "--input",
                    metavar="input_file",
                    dest="name_file",
                    type=str,
                    #required=True,
                    help="file of name list to transfer")
parser.add_argument(
                    "-g",
                    "-gene",
                    "--gene",
                    action='append',
                    dest='gene_list',
                    default=[],
                    help='Add gene ids to a list')
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

Gene_dict = {}
with open("RAP-MSU.txt") as IN:
    for line in IN:
        line = line.strip()
        if line == '':
            continue
        columns = line.split("\t")
        Gene_dict[columns[0]] = columns[1]

Name_file = ''
try:
    Name_file = args.name_file
except:
    pass
if Name_file != None:
    with open(Name_file) as IN:
        for gene in IN:
            gene = gene.strip()
            if gene == '':
                continue
            if gene[0:2] == 'Os':
                locus = re.sub("\.\d+$", '', gene)
                if locus in Gene_dict.keys():
                    print("%s\t%s" % (gene, Gene_dict[locus]))
                else:
                    print("%s\tNone" % gene)
            elif gene[0:3] == "LOC":
                flag = 0
                for key in sorted(Gene_dict.keys()):
                    if gene in Gene_dict[key]:
                        flag = 1
                        print("%s\t%s" % (gene, key))
                if flag == 0:
                    print("%s\tNone" % gene)
            else:
                print("Ilegal gene id: %s" % gene)

for gene in args.gene_list:
    if gene[0:2] == 'Os':
        locus = re.sub("\.\d+$", '', gene)
        if locus in Gene_dict.keys():
            print("%s\t%s" % (gene, Gene_dict[locus]))
        else:
            print("%s\tNone!" % gene)
    elif gene[0:3] == "LOC":
        flag = 0
        for key in sorted(Gene_dict.keys()):
            if gene in Gene_dict[key]:
                flag = 1
                print("%s\t%s" % (gene, key))
        if flag == 0:
            print("%s\tNone" % gene)
    else:
        print("Ilegal gene id: %s" % gene)